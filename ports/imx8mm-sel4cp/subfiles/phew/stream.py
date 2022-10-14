"""
A simple stream class for the Phew framework.
"""

import cptxrx

verbose = True

def p(*args):
    if verbose:
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
    def __init__(self):
        pass

    def write(self, data):
        cptxrx.tx(data)
    
    def writefile(self, file):
        cptxrx.txfile(file)

    def writefilerange(self, file, start, end):
        cptxrx.txfilerange(file, start, end)
