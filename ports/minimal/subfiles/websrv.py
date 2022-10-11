from phew import server
from phew.server import FileResponse
from phew.template import render_template
import cpringbuf as cprb


# basic response with status code and content type
@server.route("/", methods=["GET"])
def basic(request):
  a = b''.join([x for x in render_template("index.html", name="World")])
  return a, 200, "text/html"

@server.route("/hello", methods=["GET"])
def hello(request):
  return "Hello, world!", 200, "text/html"

@server.route("/page/<subpage>", methods=["GET"])
def hello_name(request, subpage):
  a = b"".join([x for x in render_template("sel4template", page_name=subpage)])
  return a, 200, "text/html"

@server.route("/styles/<name>", methods=["GET"])
def style_files(request, name):
  print("Serving file", f"/styles/{name}")
  return FileResponse(f"/styles/{name}")

# catchall example
@server.catchall()
def catchall(request):
  return "Not found", 404

from phew.stream import Reader, Writer
from phew.server import handle_request

writer = Writer(b'')
handle_request(Reader(b"GET /page/home HTTP/1.1\r\nHost: www.tutorialspoint.com\r\nAccept-Language: en-us\r\n\r\n"), writer)
print(writer.stream.decode())