import cpfs

def render_template(template, **kwargs):
  data = cpfs.readfile('templates/' + template).encode('utf-8')
  # read the whole template file, we could work on single lines but
  # the performance is much worse - so long as our templates are
  # just a handful of kB it's ok to do this
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
    try:
      if expression.decode("utf-8") in params:
        result = params[expression.decode("utf-8")]
        result = result.replace("&", "&amp;")
        result = result.replace('"', "&quot;")
        result = result.replace("'", "&apos;")
        result = result.replace(">", "&gt;")
        result = result.replace("<", "&lt;")
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
          yield str(result).encode("utf-8")
    except:
      pass

    # discard the parsed bit
    token_caret = end + 2

# logging.debug("> parsed template:", template, "(took", time.ticks_ms() - start_time, "ms)")