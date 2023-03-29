exit(1)
# from phew import server
# from phew.stream import Reader

# from metadata.breadcrumbs import breadcrumbs
# from metadata.nav import nav

# from phew.stream import p
# import cptxrx
# import cpfs as fs
# from sDDF.echo_server.micropython.ports.minimal.subfiles.phew.server import FileResponse

# def make_breadcrumbs(page_name):
#   # We assume that the page exists
#   pages = page_name.split('/')
#   crumbs = []
#   if len(pages) == 0:
#     return []
#   else:
#     crumbs = breadcrumbs[pages[0]][pages[1]]
#   print("Crumbs", crumbs)
#   res = b"\n<ul>\n"
#   for item in crumbs:
#     res += b'\t<li href="' + item['url'] + b'">' + item['name'] + b'</li>\n'
#   res += b'</ul>\n'
#   return res


# def render_nav():
#   res = b'<ul>'
#   for item in nav:
#     res += b'<li><a href="' + item['url'] + b'">' + item['name'] + b'</a></li>'
#     if (item['children'] != None):
#       res += b'<ul>'
#       for child in item['children']:
#         res += b'<li><a href="' + child['url'] + b'">' + child['name'] + b'</a></li>'
#       res += b'</ul>'
#   res += b'</ul>'
#   return res

# def page_response(page_name, addBreadcrumbs=True):
#   content = b''
#   content += fs.readfile('/templates/sel4header.html')
#   content += render_nav()
#   if addBreadcrumbs:
#     content += make_breadcrumbs(page_name)
#   content += fs.readfile('/content/' + page_name + '.html')
#   content += fs.readfile('/templates/sel4footer.html')

#   return content





# @server.route('/', methods=['GET'])
# def index(request):
#   return page_response('index', addBreadcrumbs=False), 200, 'text/html'

# @server.route('/[page_name]', methods=['GET'])
# def page(request, page_name):
#   p("Page name", page_name)
#   if '.' in page_name:
#     return "Not found", 404
#   if page_name == '':
#     page_name = 'index'
#   stat = fs.stat("content/" + page_name + ".html")
#   if isinstance(stat, int):
#     stat = fs.stat("content/" + page_name)
#   if isinstance(stat, int):
#     return "Not found", 404
#   elif stat[3] == 1:
#     page_name = page_name + "/index"
#   return page_response(page_name), 200, 'text/html'


# @server.route('/css/[file_name]', methods=['GET'])
# def css(request, file_name):
#   return FileResponse('content/css/' + file_name)

# # @server.route("/[page_name]", methods=["GET"])
# # def page_server(request, page_name):
# #   if (not template_exists(page_name)):
# #     return "Not found", 404
# #   a = b"".join([x for x in render_template("sel4template", page_name=page_name)])
# #   return a, 200, "text/html"

# # catchall example
# @server.catchall()
# def catchall(request):
#   return "Not found", 404

# from phew.stream import Reader, Writer
# from phew.server import handle_request

# writer = Writer()
# handle_request(Reader(cptxrx.rx()), writer)