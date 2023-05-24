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
    filePath = "/content/" + pagePath + ".html"
    fs.statasync(filePath)

    return {
        "page_req": 1,
        "pagePath": pagePath,
        "filePath": filePath,
        "addBreadcrumbs": addBreadcrumbs,
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
    return page_response(request, "index", addBreadcrumbs=False)


@server.route("/[pagePath]", methods=["GET"])
def page(request, pagePath):
    isFile = pagePath.split(".")[-1] in supportedFileTypes
    pagePath = standardise_path(pagePath, isFile)

    if (pagePath == ""):
        return "Not found", 404
    elif (isFile):
        return file_response(request, pagePath)
    else:
        return page_response(request, pagePath)

# catchall example
@server.catchall()
def catchall(request):
    return "Not found", 404


from phew.stream import Reader, Writer
from phew.server import handle_request

writer = Writer()
handle_request(Reader(cptxrx.rx()), writer)
