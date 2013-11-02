"""
The Node object
"""


class Node(object):
    def __init__(self, name=None, *children, **attr):
        self.name = name or ""
        self.attr = attr
        self.children = list(children)

    def __repr__(self):
        contents = []
        for key, val in sorted(self.attr.iteritems()):
            contents.append('{0!s}={0!r}'.format(key, val))
        for val in self.attr:
            contents.append(repr(val))
        return "{0}({1})".format(self.name, ', '.join(contents))

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        for attr in ('name', 'children', 'attr'):
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def __getitem__(self, key):
        return self.children[key]

    def __iter__(self):
        return iter(self.children)

    def __len__(self):
        return len(self.children)

    def __contains__(self, item):
        return item in self.children
