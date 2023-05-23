from phew import server
from phew.server import FileResponse
from phew.stream import Reader
from metadata.breadcrumbs import breadcrumbs

import time

import continuation

from phew.stream import p
import cptxrx
import cpfs as fs

supportedFileTypes = {"ico", "css", "js", "png", "pdf", "jpg", "jpeg", "gif", "svg"}

def page_response(request, pagePath, addBreadcrumbs=True):
    print("Got page request")
    # continuationstore(request)
    # fs.readfileasync("/content/" + pagePath + ".html")
    
    filePath = "/content/" + pagePath + ".html"
    fs.statasync(filePath)

    return {
        "page_req": 1,
        "pagePath": pagePath,
        "filePath": filePath,
        "addBreadcrumbs": addBreadcrumbs
    }

def file_response(request, pagePath):
    filePath = "/content/" + pagePath
    fs.statasync(filePath)

    return {
        "page_req": 0,
        "pagePath": pagePath,
        "filePath": filePath,
        "addBreadcrumbs": False,
    }

def standardise_path(path:str, isFile:bool):
    if path.startswith("/"):
        path = path[1:]
    if path.endswith("/"):
        path = path[:-1]
    
    if (isFile):
        return path
    
    if (path == ""):
        return "index"
    elif (path.endswith(".html")):
        path = path[:-5]
    elif (path.endswith(".htm")):
        path = path[:-4]
    
    # If path is to a directory, add 'index' to the end. Breadcrumbs.py holds the sitemap
    pathParts = path.split("/")
    currPart = breadcrumbs
    isList = True

    # We do a loop for if in future we add deeper pages
    for part in pathParts:
        if (part in currPart):
            currPart = currPart[part]
            isList = type(currPart) == list
        else:
            return ""

    if (not isList):
        path += "/index"

    return path


@server.route("/", methods=["GET"])
def index(request):
    print("Got index request")
    return page_response(request, "index", addBreadcrumbs=False)


@server.route("/[pagePath]", methods=["GET"])
def page(request, pagePath):
    print(f"Serving {pagePath}")
    isFile = pagePath.split(".")[-1] in supportedFileTypes
    print(f"Is file: {isFile}")
    pagePath = standardise_path(pagePath, isFile)
    print(f"Standardised path: {pagePath}")

    if (pagePath == ""):
        return "Not found", 400
    elif (isFile):
        return file_response(request, pagePath)
    else:
        return page_response(request, pagePath)
    
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


# @server.route("/favicon.ico", methods=["GET"])
# def favicon(request):
#     return FileResponse("images/favicon.ico")


# @server.route("/about/seL4-whitepaper.pdf", methods=["GET"])
# def seL4_whitepaper(request):
#     p("Got whitepaper request")
#     return FileResponse("templates/about/seL4-whitepaper.pdf", request.headers)


# @server.route("/css/<name>", methods=["GET"])
# def style_files(request, name):
#     print("Got style file request", name)
#     return FileResponse(f"content/css/{name}")


# @server.route("/js/<name>", methods=["GET"])
# def script_files(request, name):
#     return FileResponse(f"content/js/{name}")


# @server.route("/images/[name]", methods=["GET"])
# def image_files(request, name):
#     return FileResponse(f"content/images/{name}")


# @server.route("/docs/<group>/<name>", methods=["GET"])
# def docs_files(request, group, name):
#     return FileResponse(f"content/docs/{group}/{name}")


# catchall example
@server.catchall()
def catchall(request):
    return "Not found", 404


from phew.stream import Reader, Writer
from phew.server import handle_request

writer = Writer()
handle_request(Reader(cptxrx.rx()), writer)
