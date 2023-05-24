import continuation
from phew.server import handle_request_cb
from phew.stream import Writer
from phew.server import Request
import cpfs

privData = continuation.loadprivatedata()

status = continuation.getstatus()

if status == 0:
    stat = continuation.stat()   
    cpfs.readfileasync(privData["filePath"], stat[0])
else:
    # Stat failed, file not found, hence return a 404
    handle_request_cb(Writer(), Request("GET", privData["uri"], "HTTP/1.1"), ("Not found", 404))
