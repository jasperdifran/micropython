from phew import server
from phew.server import FileResponse
from phew.stream import Reader

import time

import continuation

from phew.stream import p
import cptxrx
import cpfs as fs


def page_response(request, page_name, addBreadcrumbs=True):
    print("Got page request")
    # continuation.store(request)
    # fs.readfileasync("/content/" + page_name + ".html")
    fs.statasync("/content/" + page_name + ".html")

    return {
        "page_req": 1,
        "uri": request.uri,
    }


@server.route("/", methods=["GET"])
def index(request):
    print("Got index request")
    return page_response(request, "index", addBreadcrumbs=False)


@server.route("/[page_name]", methods=["GET"])
def page(request, page_name):
    print("Got page request")
    if "." in page_name:
        return "Not found", 404
    stat = fs.stat("content/" + page_name + ".html")
    if isinstance(stat, int):
        stat = fs.stat("content/" + page_name)
    if isinstance(stat, int):
        return "Not found", 404
    elif stat[3] == 1:
        page_name = page_name + "/index"
    return page_response(request, page_name), 200, "text/html"


@server.route("/favicon.ico", methods=["GET"])
def favicon(request):
    return FileResponse("images/favicon.ico")


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
