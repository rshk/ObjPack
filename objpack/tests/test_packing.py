import json

import pytest

import objpack
from .fixtures import objects, json_objects


pytest.skip()


def test_pack_simple(objects):
    """Simple packing / unpacking test"""
    for obj in objects:
        assert objpack.loads(objpack.dumps(obj)) == obj


def test_pack_json(json_objects):
    """Try unpacking as Json some compatible objects"""
    for obj in json_objects:
        assert json.loads(objpack.dumps(obj)) == obj
