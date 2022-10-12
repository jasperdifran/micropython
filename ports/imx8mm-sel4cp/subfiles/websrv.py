from phew import server
from phew.server import FileResponse
from phew.template import render_template, template_exists
import cptxrx

@server.route("/[page_name]", methods=["GET"])
def page_server(request, page_name):
  if (not template_exists(page_name)):
    return "Not found", 404
  a = b"".join([x for x in render_template("sel4template", page_name=page_name)])
  return a, 200, "text/html"

@server.route("/styles/<name>", methods=["GET"])
def style_files(request, name):
  return FileResponse(f"/styles/{name}")

@server.route("/scripts/<name>", methods=["GET"])
def script_files(request, name):
  return FileResponse(f"/scripts/{name}")

# catchall example
@server.catchall()
def catchall(request):
  return "Not found", 404

from phew.stream import Reader, Writer
from phew.server import handle_request

writer = Writer()
handle_request(Reader(cptxrx.rx()), writer)