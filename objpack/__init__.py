"""
ObjPack main package
"""

# Bring Node in the main namespace
from .node import Node, create_node


def load(fp):
    """
    :param fp: a file-like object, to be read
    :return: the deserialized object
    """
    return loads(fp.read())


def loads(s):
    """
    :param s: a string to be parser
    :return: the deserialized object
    """
    from objpack.lexer import lexer
    from objpack.parser import parser
    return parser.parse(s, lexer=lexer)


def dump(obj, fp):
    """
    :param obj: the object to be serialized
    :param fp: file-like object to which to write
    """
    fp.write(dumps(obj))


def dumps(obj):
    """
    :param obj: object to be serialized
    :return: a string containing the serialized object
    """
    from objpack.serializer import serialize
    return serialize(obj)


# For compatibility with other libraries
pack = dump
packs = dumps
unpack = load
unpacks = loads
