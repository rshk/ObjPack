import pytest

from objpack import Node, create_node


def test_node_object():
    node = Node.with_name('Example')
    assert node.name == 'Example'
    assert node.attr == {}
    assert node.children == []
    node == Node.with_name('Example')

    Example = create_node('Example')
    node = Example('one', 'two', attr='val', attr1='val1')
    assert node.name == 'Example'
    assert node.attr == {'attr': 'val', 'attr1': 'val1'}
    assert node.children == ['one', 'two']
    assert node == Example('one', 'two', attr='val', attr1='val1')

    assert Example('a', 'b') == Node.with_name('Example', 'a', 'b')

    assert len(node) == 2
    children = []
    for item in node:
        children.append(item)
    assert children == node.children

    assert repr(node) == "Example(attr='val', attr1='val1', 'one', 'two')"

    # Just to test inequality..
    assert node != "Hello"
    assert node != object()
    assert node != Node.with_name('AnotherNode')
    Example = create_node('Example')
    assert node != Example()
    assert node != Example('one', 'two')
    assert node != Example(attr='val', attr1='val1')
    assert node[0] == 'one'
    assert node[1] == 'two'
    with pytest.raises(IndexError):
        node[2]
    assert 'one' in node
    assert 'two' in node
