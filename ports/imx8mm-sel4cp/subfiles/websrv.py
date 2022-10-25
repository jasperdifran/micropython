
from phew import server
from phew.server import FileResponse
from phew.template import render_template, template_exists
from phew.stream import Reader

from metadata.breadcrumbs import breadcrumbs
from metadata.nav import nav
from metadata.page_title import page_title

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
  print("Crumbs", crumbs)
  res = b"\n<ul>\n"
  for item in crumbs:
    res += b'\t<li><a href="' + item['url'] + b'">' + item['name'] + b'</a></li>\n'
  res += b'</ul>\n'
  return res


def render_nav(page_name):
  res = b''
  group = page_name.split('/')[0]

  for item in nav:
    activeClass = b'active' if item['url'].decode()[1:].startswith(group) else b''
    if page_name == 'index':
      activeClass = b'active' if item['url'] == b'/' else b''

    # res += b'<li><a href="' + item['url'] + b'">' + item['name'] + b'</a></li>'
    if (item['children'] and item['children'] != []):
      res += b'<li class="dropdown ' + activeClass + '"><a class="dropdown-toggle" data-toggle="dropdown" href="' + item['url'] + '">' + item['name'] + ' <span class="caret"></span></a>'
      res += b'<ul class="dropdown-menu">'
      for child in item['children']:
        res += b'<li><a href="' + child['url'] + b'">' + child['name'] + b'</a></li>'
      res += b'</ul></li>'
    else:
      res += b'<li class="' + activeClass + '"><a href="' + item['url'] + b'">' + item['name'] + b'</a></li>'
  return res

def page_response(page_name, addBreadcrumbs=True):
  navigation = render_nav(page_name)
  breadcrumbs = make_breadcrumbs(page_name) if addBreadcrumbs else b''
  title = page_title[page_name]
  page_content = fs.readfile('/content/' + page_name + '.html')
  content = b''.join([b for b in render_template('sel4header.html', \
    navigation=navigation, breadcrumbs=breadcrumbs, title=title, page_content=page_content)])
  return content

@server.route('/', methods=['GET'])
def index(request):
  return page_response('index', addBreadcrumbs=False), 200, 'text/html'

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
  print("Got style file request", name)
  return FileResponse(f"content/css/{name}")

@server.route("/js/<name>", methods=["GET"])
def script_files(request, name):
  return FileResponse(f"content/js/{name}")

@server.route("/images/[name]", methods=["GET"])
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