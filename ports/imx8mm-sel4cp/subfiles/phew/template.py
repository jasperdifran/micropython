import cpfs
from phew.server import pdict

def render_template(template, **kwargs):
  # read the whole template file, we could work on single lines but
  # the performance is much worse - so long as our templates are
  # just a handful of kB it's ok to do this
  data = cpfs.readfile('templates/' + template + ".html")
  token_caret = 0

  while True:
    # find the next tag that needs evaluating
    start = data.find(b"{{", token_caret)
    end = data.find(b"}}", start)

    match = start != -1 and end != -1

    # no more magic to handle, just return what's left
    if not match:
      yield data[token_caret:]
      break

    expression = data[start + 2:end].strip()

    # output the bit before the tag
    yield data[token_caret:start]

    # merge locals with the supplied named arguments and
    # the response object
    params = {}
    params.update(locals())
    params.update(kwargs)
    # params["response"] = response

    # parse the expression
    if expression.decode("utf-8") in params:
      result = params[expression.decode("utf-8")]
      # result = result.replace(b"&", b"&amp;")
      # result = result.replace(b'"', b"&quot;")
      # result = result.replace(b"'", b"&apos;")
      # result = result.replace(b">", b"&gt;")
      # result = result.replace(b"<", b"&lt;")
    else:
      if expression.startswith(b"render_template"):
        if (expression[16] == ord("'") or expression[16] == ord('"')):
          result = render_template(expression[17:-2].decode("utf-8"), **kwargs)
        else:
          result = render_template(params[expression[16:-1].decode("utf-8")], **kwargs)
      else:
        result = eval(expression, globals(), params)

    if type(result).__name__ == "generator":
      # if expression returned a generator then iterate it fully
      # and yield each result
      for chunk in result:
        yield chunk
    else:
      # yield the result of the expression
      if result:
        yield result

    # discard the parsed bit
    token_caret = end + 2


def template_exists(template):
  return cpfs.exists('templates/' + template + ".html")