import json

import pytest

import objpack
from objpack.node import Node, create_node

from .fixtures import objects, json_objects


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
    Hello = create_node('Hello')
    assert objpack.loads("Hello()") == Hello()
    assert objpack.loads("Hello('world')") == Hello('world')
    assert objpack.loads("Hello('world', example=1)") \
        == Hello('world', example=1)
    assert objpack.loads("Hello(example=1, 'world')") \
        == Hello('world', example=1)
    assert objpack.loads("Hello(example=1)") \
        == Hello(example=1)
    assert objpack.loads("Hello(\n\texample=1\n)") \
        == Hello(example=1)


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


def test_unpack_pseudo_html():
    data = """
    Html(
        Head(
            Title("This is a title"),
            Link(rel='stylesheet', type='text/css', href='style.css')
        ),
        Body(
            H1("The main headline"),
            Table(
                class="nice-table",
                Tr(Td("One"), Td("Two"), Td("Three")),
                Tr(Td("One2"), Td("Two2"), Td("Three2")),
                Tr(Td("One3"), Td("Two3"), Td("Three3"))
            )
        )
    )
    """
    obj = objpack.loads(data)
    assert obj.name == 'Html'
    assert len(obj.children) == 2
    assert len(obj.attr) == 0

    head = obj.children[0]
    assert head.name == 'Head'
    assert head.children[0].name == 'Title'
    assert head.children[0].children[0] == 'This is a title'
    assert head.children[1].name == 'Link'
    assert head.children[1].attr['rel'] == 'stylesheet'
    assert head.children[1].attr['type'] == 'text/css'
    assert head.children[1].attr['href'] == 'style.css'

    body = obj.children[1]
    assert body.name == 'Body'

    h1 = body.children[0]
    assert h1.name == 'H1'

    table = body.children[1]
    assert table.name == 'Table'
    assert table.attr['class'] == 'nice-table'


def test_unpack_trailing_commas():
    """Extra trailing commas are allowed in objects"""

    assert objpack.loads("[1, 2, 3, ]") == [1, 2, 3]
    with pytest.raises(TypeError):
        objpack.loads('[1, 2, 3,,]')
    with pytest.raises(TypeError):
        objpack.loads('[1, 2, , 3]')

    assert objpack.loads("{'a': 'b', 'c': 'd',}") == {'a': 'b', 'c': 'd'}

    Obj = create_node('Obj')
    assert objpack.loads("Obj('a', 'b',)") == Obj('a', 'b')
    assert objpack.loads("Obj(a='A', b='B',)") == Obj(a='A', b='B')
    assert objpack.loads("Obj(a='A', b='B', 'x', 'y',)") \
        == Obj('x', 'y', a='A', b='B')


def test_unpack_json(json_objects):
    """We should be able to properly unpack json too"""

    for obj in json_objects:
        assert objpack.loads(json.dumps(obj)) == obj
