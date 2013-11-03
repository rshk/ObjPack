import json
import sys

import pytest

import objpack
from .fixtures import objects, json_objects


## Allow failure with Python 3
xfail_py3k = pytest.mark.xfail(
    sys.version_info[0] == 3,
    reason="Python3 not yet 100% supported")


@xfail_py3k
def test_pack_simple(objects):
    """Simple packing / unpacking test"""
    for obj in objects:
        assert objpack.loads(objpack.dumps(obj)) == obj


@xfail_py3k
def test_pack_json(json_objects):
    """Try unpacking as Json some compatible objects"""
    for obj in json_objects:
        assert json.loads(objpack.dumps(obj)) == obj
