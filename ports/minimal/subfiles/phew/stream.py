# Jdf

def p(*args):
    print("P: ", *args)

class Reader:
    def __init__(self, stream):
        self.stream = stream

    def read(self, n):
        res = self.stream[:n]
        self.stream = self.stream[n:]
        return res

    def readline(self):
        endLine = self.stream.find(b"\n")
        res = self.stream[:(endLine + 1)] if endLine != -1 else self.stream
        self.stream = self.stream[(endLine + 1):] if endLine != -1 else b''
        return res

class Writer:
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream += data

    def flush(self):
        self.stream = b''
        pass

