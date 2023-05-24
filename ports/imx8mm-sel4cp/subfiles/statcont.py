import continuation
from phew.server import handle_request_cb
from phew.stream import Writer
from phew.server import Request
import cpfs

privData = continuation.loadprivatedata()

status = continuation.getstatus()
print("Got status", status)

if status == 0:
    stat = continuation.stat()

    print("stat file_size", stat[0])
    print("stat last_mod_date", stat[1])
    print("stat last_mod_time", stat[2])
    print("stat is_dir", stat[3])

    print("page_req", privData["page_req"])
    print("pagePath", privData["pagePath"])
    print("filePath", privData["filePath"])
    

    cpfs.readfileasync(privData["filePath"], stat[0])


    # cpfs.statasync("/content/" + privData["page_req"] + ".html")
else:
    # Stat failed, file not found, hence return a 404
    handle_request_cb(Writer(), Request("GET", privData["uri"], "HTTP/1.1"), ("Not found", 404))
