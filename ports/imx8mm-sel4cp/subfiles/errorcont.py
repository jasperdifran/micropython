import continuation
from phew.server import handle_request_cb
from phew.stream import Writer
from phew.server import Request, status_message_map

status = continuation.getstatus()
print("Got status", status)
privData = continuation.loadprivatedata()

handle_request_cb(Writer(), Request("GET", privData["pagePath"], "HTTP/1.1"), (status_message_map[status] if status in status_message_map else 500, status))