import pytest

from objpack import Node


@pytest.fixture
def json_objects():
    return [
        123,
        3.1415,
        "Hello, world!",
        #Hello,\nworld!",  # not supported yet
        [1, 2, 3],
        True,
        False,
        None,
        ['a', 'b', 'c'],
        [1, 'a', ['x', 'y']],
        {'a': 'b', 'c': 'd'},
        {'a': [1, 2, 3], 'c': [4, 5, 6]},
        {'a': {'1': 'A', '2': 'B'}, 'b': 'XX', 'c': 22},
    ]


@pytest.fixture
def objects():
    return json_objects() + [
        Node(),
        Node('Example'),
        Node('Example', 'first'),
        Node('Example', 'first', 'second'),
        Node('Example', param1='value1'),
        Node('Example', param1='value1', param2='value2'),
        Node('Example',
             'first',
             'second',
             param1='value1',
             param2='value2'),
        {
            'hello': Node('World', name='earth'),
            'example': Node('Website', url='http://www.example.com'),
        },
    ]
