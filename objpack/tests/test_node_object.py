import pytest

from objpack import Node


def test_node_object():
    node = Node('Example')
    assert node.name == 'Example'
    assert node.attr == {}
    assert node.children == []
    node == Node('Example')

    node = Node('Example', 'one', 'two', attr='val', attr1='val1')
    assert node.name == 'Example'
    assert node.attr == {'attr': 'val', 'attr1': 'val1'}
    assert node.children == ['one', 'two']
    assert node == Node('Example', 'one', 'two', attr='val', attr1='val1')

    assert len(node) == 2
    children = []
    for item in node:
        children.append(item)
    assert children == node.children

    assert repr(node) == "Example(attr='val', attr1='val1', 'one', 'two')"

    # Just to test inequality..
    assert node != "Hello"
    assert node != object()
    assert node != Node('AnotherNode')
    assert node != Node('Example')
    assert node != Node('Example', 'one', 'two')
    assert node != Node('Example', attr='val', attr1='val1')
    assert node[0] == 'one'
    assert node[1] == 'two'
    with pytest.raises(IndexError):
        node[2]
    assert 'one' in node
    assert 'two' in node
