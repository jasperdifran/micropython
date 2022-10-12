import cpfs

def render_template(template, **kwargs):
  print("Rendering template: " + template)
  # read the whole template file, we could work on single lines but
  # the performance is much worse - so long as our templates are
  # just a handful of kB it's ok to do this
  data = cpfs.readfile('templates/' + template + ".html")
  # print("Template", template, "data", data)
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
    # print("Something happened")
    # try:
    if expression.decode("utf-8") in params:
      # print("Found something, not an expression")

      result = params[expression.decode("utf-8")]
      result = result.replace("&", "&amp;")
      result = result.replace('"', "&quot;")
      result = result.replace("'", "&apos;")
      result = result.replace(">", "&gt;")
      result = result.replace("<", "&lt;")
    else:
      # print("Trying an expression")
      # print("Expression", expression)
      # print("Params", params)
      # print("Globals", globals())
      if expression.startswith(b"render_template"):
        print("expr", expression)
        if (expression[16] == ord("'") or expression[16] == ord('"')):
          print("looking for template:", expression[17:-2])
          result = render_template(expression[17:-2].decode("utf-8"), **kwargs)
        else:
          print("looking for var:", expression[16:-1])
          result = render_template(params[expression[16:-1].decode("utf-8")], **kwargs)
      else:
        result = b''
      # res = eval("retval()", globals(), params)
      # print("Result", res)
      # result = eval(expression, globals(), params)
      # print("Got result", result)

    if type(result).__name__ == "generator":
      # if expression returned a generator then iterate it fully
      # and yield each result
      for chunk in result:
        yield chunk
    else:
      # yield the result of the expression
      if result:
        yield str(result).encode("utf-8")
    # except:
    #   print("Error evaluating expression", expression)
    #   pass

    # discard the parsed bit
    token_caret = end + 2

# logging.debug("> parsed template:", template, "(took", time.ticks_ms() - start_time, "ms)")