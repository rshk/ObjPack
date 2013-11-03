import pytest

from objpack import Node


@pytest.fixture
def json_objects():
    return [
        123,
        3.1415,
        u"Hello, world!",
        #Hello,\nworld!",  # not supported yet
        [1, 2, 3],
        True,
        False,
        None,
        [u'a', u'b', u'c'],
        [1, u'a', [u'x', u'y']],
        {u'a': u'b', u'c': u'd'},
        {u'a': [1, 2, 3], u'c': [4, 5, 6]},
        {u'a': {u'1': u'A', u'2': u'B'}, u'b': u'XX', u'c': 22},
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
