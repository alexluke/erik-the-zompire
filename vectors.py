import numpy

def vector(x,y=None):
    if y==None: return numpy.array(x)
    else: return numpy.array((x,y))
    
def vlen(v):
    return numpy.sqrt(numpy.dot(v,v))

def normalize(v):
    v = numpy.array(v)
    length = vlen(v)
    if length == 0: return v
    else: return v/length
    
def cross(a,b):
    return cross_product(a,b)
