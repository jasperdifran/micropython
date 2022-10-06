from phew import server
import cpringbuf as c

# basic response with status code and content type
@server.route("/", methods=["GET"])
def basic(request):
  return "Gosh, a request", 200, "text/html"

@server.route("/hello", methods=["GET"])
def hello(request):
  return "Hello, world!", 200, "text/html"

# catchall example
@server.catchall()
def catchall(request):
  return "Not found", 404

from phew.stream import Reader, Writer
from phew.server import handle_request

writer = Writer(b'')
handle_request(Reader(c.rx().encode()), writer)
c.tx(writer.stream)


# writer = Writer(b'')
# handle_request(Reader(b"GET /hello HTTP/1.1\r\nHost: www.tutorialspoint.com\r\nAccept-Language: en-us\r\n\r\n"), writer)
# c.tx(writer.stream)
