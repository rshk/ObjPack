import json
import sys

import pytest

import objpack
from objpack.serializer import serialize
from .fixtures import objects, json_objects


## Allow failure with Python 3
xfail_py3k = pytest.mark.xfail(
    sys.version_info[0] == 3,
    reason="Python3 not yet 100% supported")


def test_pack_simple():
    assert serialize(1234) == '1234'
    #assert objpack.dumps(u'abc') == '"abc"'
    assert serialize(b'abc') == 'b"abc"'
    assert serialize(b'\x00\x01\x02\x03') == r'b"\x00\x01\x02\x03"'
    pass


#@xfail_py3k
def test_pack_unpack(objects):
    """Simple packing / unpacking test"""
    for obj in objects:
        assert objpack.loads(objpack.dumps(obj)) == obj


#@xfail_py3k
def test_pack_unpack_json_compat(json_objects):
    """Try unpacking as Json some compatible objects"""
    for obj in json_objects:
        assert json.loads(objpack.dumps(obj)) == obj
