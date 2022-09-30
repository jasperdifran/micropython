
from phew import server

# basic response with status code and content type
@server.route("/", methods=["GET"])
def basic(request):
  return "Gosh, a request", 200, "text/html"

@server.route("/hello", methods=["GET"])
def hello(request):
  return "Hello, world!", 200, "text/html"

from phew.stream import Reader, Writer
from phew.server import handle_request

writer = Writer(b'')
handle_request(Reader(b"GET / HTTP/1.1\r\nHost: www.tutorialspoint.com\r\nAccept-Language: en-us\r\n\r\n"), writer)
print(writer.stream)


writer = Writer(b'')
handle_request(Reader(b"GET /hello HTTP/1.1\r\nHost: www.tutorialspoint.com\r\nAccept-Language: en-us\r\n\r\n"), writer)
print(writer.stream)
