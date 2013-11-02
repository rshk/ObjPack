"""
ObjPack main package
"""


def load(fp):
    return loads(fp.read())


def loads(s):
    from objpack.parser import parser, lexer
    return parser.parse(s, lexer=lexer)


def dump(obj, fp):
    fp.write(dumps(obj))


def dumps(obj):
    pass
