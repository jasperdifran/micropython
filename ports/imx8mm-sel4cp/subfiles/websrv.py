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

@server.route("/hello/<name>", methods=["GET"])
def hello_name(request, name):
  a = b"".join([x for x in render_template("example.html", name=name)])
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
handle_request(Reader(cprb.rx().encode()), writer)
cprb.tx(writer.stream)