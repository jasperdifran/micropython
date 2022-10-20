
from phew import server
from phew.server import FileResponse
from phew.template import render_template, template_exists
from phew.stream import Reader

from metadata.breadcrumbs import breadcrumbs
from metadata.nav import nav

from phew.stream import p
import cptxrx
import cpfs as fs

def make_breadcrumbs(page_name):
  # We assume that the page exists
  pages = page_name.split('/')
  crumbs = []
  if len(pages) == 0:
    return []
  else:
    crumbs = breadcrumbs[pages[0]][pages[1]]

  res = b"<ul>"
  for item in crumbs:
    res += b'<li href="' + item['url'] + b'">' + item['name'] + b'</li>'
  res += b'</ul>'
  return res


def render_nav():
  res = b'<ul>'
  for item in nav:
    res += b'<li href="' + item['url'] + b'">' + item['name'] + b'</li>'
    if (item['children'] != None):
      res += b'<ul>'
      for child in item['children']:
        res += b'<li href="' + child['url'] + b'">' + child['name'] + b'</li>'
      res += b'</ul>'
  res += b'</ul>'
  return res

def page_response(page_name):
  content = b''
  content += fs.readfile('/templates/sel4header.html')
  content += render_nav()
  content += make_breadcrumbs(page_name)
  content += fs.readfile('/content/' + page_name + '.html')
  content += fs.readfile('/templates/sel4footer.html')
  return content

@server.route('/[page_name]', methods=['GET'])
def page(request, page_name):
  if '.' in page_name:
    return "Not found", 404
  stat = fs.stat("content/" + page_name + ".html")
  if isinstance(stat, int):
    stat = fs.stat("content/" + page_name)
  if isinstance(stat, int):
    return "Not found", 404
  elif stat[3] == 1:
    page_name = page_name + "/index"
  return page_response(page_name), 200, 'text/html'

@server.route('/favicon.ico', methods=['GET'])
def favicon(request):
  return FileResponse('images/favicon.ico')

@server.route("/about/seL4-whitepaper.pdf", methods=["GET"])
def seL4_whitepaper(request):
  p("Got whitepaper request")
  return FileResponse("templates/about/seL4-whitepaper.pdf", request.headers)

@server.route("/css/<name>", methods=["GET"])
def style_files(request, name):
  return FileResponse(f"content/css/{name}")

@server.route("/js/<name>", methods=["GET"])
def script_files(request, name):
  return FileResponse(f"content/js/{name}")

@server.route("/img/<name>", methods=["GET"])
def image_files(request, name):
  return FileResponse(f"content/images/{name}")

@server.route("/docs/<group>/<name>", methods=["GET"])
def docs_files(request, group, name):
  return FileResponse(f"content/docs/{group}/{name}")

# catchall example
@server.catchall()
def catchall(request):
  return "Not found", 404

from phew.stream import Reader, Writer
from phew.server import handle_request

writer = Writer()
handle_request(Reader(cptxrx.rx()), writer)