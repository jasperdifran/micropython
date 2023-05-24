import continuation
from phew.server import handle_request_cb
from phew.stream import Writer
from phew.server import Request

status = continuation.getstatus()
print("Got status", status)
privData = continuation.loadprivatedata()

if (status == 500):
    handle_request_cb(Writer(), Request("GET", privData["pagePath"], "HTTP/1.1"), ("Internal Server Error", 500))