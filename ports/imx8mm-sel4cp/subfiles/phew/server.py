# Phew
from phew.stream import p
import cpfs 

content_len_max = 1024 * 128 # 128kb

_routes = []
catchall_handler = None

def pdict(d):
  p("{")
  for key, val in d.items():
    p("\t", key, ":", val)
  p("}")

def urldecode(text):
  text = text.replace("+", " ")
  result = ""
  token_caret = 0
  # decode any % encoded characters
  while True:
    start = text.find("%", token_caret)
    if start == -1:
      result += text[token_caret:]
      break
    result += text[token_caret:start]
    code = int(text[start + 1:start + 3], 16)
    result += chr(code)
    token_caret = start + 3
  return result

def _parse_query_string(query_string):
  result = {}
  for parameter in query_string.split("&"):
    key, value = parameter.split("=", 1)
    key = urldecode(key)
    value = urldecode(value)
    result[key] = value
  return result


class Request:
  def __init__(self, method, uri, protocol):
    self.method = method
    self.uri = '/index' if uri == '/' else uri
    self.protocol = protocol
    self.form = {}
    self.data = {}
    self.query = {}
    query_string_start = self.uri.find("?") if self.uri.find("?") != -1 else len(self.uri)
    self.path = self.uri[:query_string_start]
    self.query_string = self.uri[query_string_start + 1:]
    if self.query_string:
      self.query = _parse_query_string(self.query_string)

  def __str__(self):
    return f"""\
request: {self.method} {self.path} {self.protocol}
headers: {self.headers}
form: {self.form}
data: {self.data}"""


class Response:
  def __init__(self, body, status=200, headers={}):
    self.status = status
    self.headers = headers
    self.body = body

  def add_header(self, name, value):
    self.headers[name] = value

  def __str__(self):
    return f"""\
status: {self.status}
headers: {self.headers}
body: {self.body}"""


content_type_map = {
  "html": "text/html",
  "jpg": "image/jpeg",
  "jpeg": "image/jpeg",
  "svg": "image/svg+xml",
  "json": "application/json",
  "png": "image/png",
  "css": "text/css",
  "js": "text/javascript",
  "csv": "text/csv",
  "pdf": "application/pdf",
}


class FileResponse(Response):
  def __init__(self, file, req_headers={}):
    self.status = 404
    self.headers = {
      "Content-Length": 0
    }
    self.file = file
    self.range_start = 0
    self.range_end = 0
    self.chunked = False

    p("Req headers")
    pdict(req_headers)

    p("FileResponse:", file)
    response = cpfs.stat(self.file)
    p("Some response:", response)
    if isinstance(response, tuple):
      # Check if there's a range header
      if response[3] == 1:
        self.headers["Content-Length"] = 0
        p("Directory")
        return
      if "range" in req_headers:
        range_header = req_headers["range"]
        # self.range_start = int(range_header[6:range_header.find("-")])

        range = range_header[6:]
        range_split = range.split("-")
        if len(range_split[1]) > 0:
          self.range_end = int(range_split[1])
        else:
          self.range_end = response[0] - 1
        self.range_start = int(range_split[0])
        # self.range_end = int(range_header[range_header.find("-") + 1:])

        # Check if requested range is too big, if so truncate it
        if self.range_end - self.range_start > content_len_max:
          self.range_end = self.range_start + content_len_max - 1

        self.status = 206
        self.headers["Content-Range"] = f"bytes {self.range_start}-{self.range_end}/{response[0]}"
        self.headers["Content-Length"] = str(self.range_end - self.range_start + 1)
        self.chunked = True
      
      # Check if requested file is too big and needs to be chunked
      elif response[0] > content_len_max:
        self.status = 206
        self.range_end = content_len_max - 1
        self.headers["Content-Range"] = f"bytes {self.range_start}-{self.range_end}/{response[0]}"
        self.headers["Content-Length"] = content_len_max
        self.chunked = True
      else:
        self.status = 200
        self.headers["Content-Length"] = response[0]

      extension = self.file.split(".")[-1].lower()
      p("Extension:", extension)
      if extension in content_type_map:
        self.headers["Content-Type"] = content_type_map[extension]
        p("Content type:", content_type_map[extension])
      # p("Processes file:", self.file)
      p("Ret headers")
      pdict(self.headers)
  
  def sendResponse(self, writer):
    p("Sending file:", self.file)
    if self.status == 206:
      if self.chunked:
        writer.writefilerange(self.file, self.range_start, self.range_end)
      else:
        pass
    elif self.status == 200:
      writer.writefile(self.file)
      pass
      


class Route:
  def __init__(self, path, handler, methods=["GET"]):
    self.path = path
    self.methods = methods
    self.handler = handler
    self.path_parts = path.split("/")
    self.path_matchall = False
    for part in self.path_parts:
      if part.startswith("["):
        self.path_matchall = True
    

  # returns True if the supplied request matches this route
  def matches(self, request):
    if request.method not in self.methods:
      return False
    compare_parts = request.path.split("/")
    if len(compare_parts) != len(self.path_parts) and not self.path_matchall:
      return False
    for part, compare in zip(self.path_parts, compare_parts):
      if (part.startswith("[")):
        return True
      if not part.startswith("<") and part != compare:
        return False
    return True

  # call the route handler passing any named parameters in the path
  def call_handler(self, request):
    parameters = {}
    compare_parts = request.path.split("/")
    for part in self.path_parts:
      value = compare_parts.pop(0)
      if part.startswith("<"):
        key = part[1:-1]
        parameters[key] = value
      elif part.startswith("["):
        key = part[1:-1]
        parameters[key] = '/'.join([value] + compare_parts)

    return self.handler(request, **parameters)
        
  def __str__(self):
    return f"""\
path: {self.path}
methods: {self.methods}
"""

  def __repr__(self):
    return f"<Route object {self.path} ({', '.join(self.methods)})>"


# parses the headers for a http request (or the headers attached to
# each field in a multipart/form-data)
def _parse_headers(reader):
  headers = {}
  while True:
    header_line = reader.readline()
    if header_line == b"\r\n": # crlf denotes body start
      break
    name, value = header_line.decode().strip().split(": ", 1)
    headers[name.lower()] = value
  return headers


# returns the route matching the supplied path or None
def _match_route(request):
  for route in _routes:
    if route.matches(request):
      return route
  return None


# if the content type is multipart/form-data then parse the fields
def _parse_form_data(reader, headers):
  boundary = headers["content-type"].split("boundary=")[1]
  # discard first boundary line
  dummy = reader.readline()

  form = {}
  while True:
    # get the field name
    field_headers = _parse_headers(reader)
    if len(field_headers) == 0:
      break
    name = field_headers["content-disposition"].split("name=\"")[1][:-1]
    # get the field value
    value = ""
    while True:
      line = reader.readline()
      line = line.decode().strip()
      # if we hit a boundary then save the value and move to next field
      if line == "--" + boundary:
        form[name] = value
        break
      # if we hit end of form data boundary then save value and return
      if line == "--" + boundary + "--":
        form[name] = value
        return form
      value += line
  return None


# if the content type is application/json then parse the body
def _parse_json_body(reader, headers):
  import json
  content_length_bytes = int(headers["content-length"])
  body = reader.readexactly(content_length_bytes)
  return json.loads(body.decode())


status_message_map = {
  200: "OK", 201: "Created", 202: "Accepted", 
  203: "Non-Authoritative Information", 204: "No Content",
  205: "Reset Content", 206: "Partial Content", 300: "Multiple Choices",
  301: "Moved Permanently", 302: "Found", 303: "See Other",
  304: "Not Modified", 305: "Use Proxy", 306: "Switch Proxy",
  307: "Temporary Redirect", 308: "Permanent Redirect",
  400: "Bad Request", 401: "Unauthorized", 403: "Forbidden",
  404: "Not Found", 405: "Method Not Allowed", 406: "Not Acceptable",
  408: "Request Timeout", 409: "Conflict", 410: "Gone",
  414: "URI Too Long", 415: "Unsupported Media Type", 
  416: "Range Not Satisfiable", 418: "I'm a teapot",
  500: "Internal Server Error", 501: "Not Implemented"
}


# handle an incoming request to the web server
def handle_request(reader, writer):
  response = None

  # request_start_time = time.ticks_ms()

  request_line = reader.readline()
  try:
    method, uri, protocol = request_line.decode().split()
  except Exception as e:
    print(f"Error parsing: {e}")
    return

  request = Request(method, uri, protocol)
  request.headers = _parse_headers(reader)
  pdict(request.headers)
  if "content-length" in request.headers and "content-type" in request.headers:
    if request.headers["content-type"].startswith("multipart/form-data"):
      request.form = _parse_form_data(reader, request.headers)
    if request.headers["content-type"].startswith("application/json"):
      request.data = _parse_json_body(reader, request.headers)
    if request.headers["content-type"].startswith("application/x-www-form-urlencoded"):
      form_data = reader.read(int(request.headers["content-length"]))
      request.form = _parse_query_string(form_data.decode()) 
    
  route = _match_route(request)
  if route:
    response = route.call_handler(request)
  elif catchall_handler:
    response = catchall_handler(request)

  response.add_header("Accept-Ranges", "bytes")

  # if shorthand body generator only notation used then convert to tuple
  if type(response).__name__ == "generator":
    response = (response,)


  # if shorthand body text only notation used then convert to tuple
  if isinstance(response, str):
    response = (response,)

  # if shorthand tuple notation used then build full response object
  if isinstance(response, tuple):
    body = response[0]
    status = response[1] if len(response) >= 2 else 200
    content_type = response[2] if len(response) >= 3 else "text/html"
    response = Response(body, status=status)
    response.add_header("Content-Type", content_type)
    # if hasattr(body, '__len__'):
    response.add_header("Content-Length", len(body))

  # write status line
  status_message = status_message_map.get(response.status, "Unknown")
  writer.write(f"HTTP/1.1 {response.status} {status_message}\r\n".encode("utf-8"))

  # write headers
  for key, value in response.headers.items():
    writer.write(f"{key}: {value}\r\n".encode("ascii"))

  # blank line to denote end of headers
  writer.write("\r\n".encode("ascii"))
  
  if isinstance(response, FileResponse):
    p("sending file")
    response.sendResponse(writer)
    # if response.status == 200:
    #   writer.writefile(response.file)
  elif type(response.body).__name__ == "generator":
    for chunk in response.body:
      writer.write(chunk)
  elif isinstance(response.body, str):
    writer.write(response.body.encode("utf-8"))
  elif isinstance(response.body, bytes):
    writer.write(response.body)
  
  # processing_time = time.ticks_ms() - request_start_time
  print(f"> {request.method} {request.path} ({response.status} {status_message}) [Sometime ms]")

# adds a new route to the routing table
def add_route(path, handler, methods=["GET"]):
  global _routes
  _routes.append(Route(path, handler, methods))
  # descending complexity order so most complex routes matched first
  _routes = sorted(_routes, key=lambda route: len(route.path_parts), reverse=True)


def set_callback(handler):
  global catchall_handler
  catchall_handler = handler


# decorator shorthand for adding a route
def route(path, methods=["GET"]):
  def _route(f):
    add_route(path, f, methods=methods)
    return f
  return _route


# decorator for adding catchall route
def catchall():
  def _catchall(f):
    set_callback(f)
    return f
  return _catchall
  

def redirect(url, status = 301):
  return Response("", status, {"Location": url})


def serve_file(file):
  return FileResponse(file)

