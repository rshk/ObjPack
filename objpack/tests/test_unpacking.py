import objpack
from objpack.parser import Node


def test_unpack_simple():
    assert objpack.loads('1') == 1
    assert objpack.loads('3.14') == 3.14
    assert objpack.loads('1024') == 1024


def test_unpack_strings():
    # Check simple strings
    assert objpack.loads('"this is a string"') == "this is a string"
    assert objpack.loads("'this is a string'") == "this is a string"

    # Check quotes "the other way round" inside strings
    assert objpack.loads('"this is \'a\' string"') == "this is 'a' string"
    assert objpack.loads("'this is \"a\" string'") == 'this is "a" string'

    # Check escapes inside strings
    assert objpack.loads('"This is \\"a string\\""') == 'This is "a string"'
    assert objpack.loads("'This is \\'a string\\''") == "This is 'a string'"

    # String auto-concatenation (C-style)
    assert objpack.loads("'Hello,' ' world'") == 'Hello, world'
    assert objpack.loads("'Hello,' \" world\"") == 'Hello, world'

    # Test escape characters
    # note: they're not supported yet!
    #assert objpack.loads('"This is \\n a newline"') == "This is \n a newline"
    #assert objpack.loads('"This is \\t a tab"') == "This is \t a tab"


def test_unpack_bool_null():
    # Boolean and None types..
    assert objpack.loads('true') is True
    assert objpack.loads('false') is False
    assert objpack.loads('null') is None


def test_unpack_lists():
    # Fun with lists
    assert objpack.loads('[]') == []
    assert objpack.loads('[1, 2, 3]') == [1, 2, 3]
    assert objpack.loads('["a", "b", "c"]') == ["a", "b", "c"]
    assert objpack.loads('[1, "abc", true, []]') == [1, 'abc', True, []]


def test_unpack_dicts():
    # Fun with dicts
    assert objpack.loads('{}') == {}
    assert objpack.loads("{'this': 'is', 'an': 'example'}") \
        == {'this': 'is', 'an': 'example'}
    assert objpack.loads("{'one': 1, 'two': 3, 'three': [1, 2, 3]}") \
        == {'one': 1, 'two': 3, 'three': [1, 2, 3]}


def test_unpack_objects():
    # Fun with objects
    assert objpack.loads("Hello()") == Node('Hello')
    assert objpack.loads("Hello('world')") == Node('Hello', 'world')
    assert objpack.loads("Hello('world', example=1)") \
        == Node('Hello', 'world', example=1)
    assert objpack.loads("Hello(example=1, 'world')") \
        == Node('Hello', 'world', example=1)
    assert objpack.loads("Hello(example=1)") \
        == Node('Hello', example=1)
    assert objpack.loads("Hello(\n\texample=1\n)") \
        == Node('Hello', example=1)


def test_unpack_comments():
    # Comments should be ignored
    assert objpack.loads("""
    # This is a comment and should be ignored.
    # I mean, "completely" ignored!
    "This is the actual text"
    """) == "This is the actual text"
    assert objpack.loads("""
    ## A configuration object
    {
        # The first option
        'hello': 'world',

        # Database configuration
        'database': 'postgresql://user:pass@host/db'
    }
    """) == {
        'hello': 'world',
        'database': 'postgresql://user:pass@host/db',
    }
