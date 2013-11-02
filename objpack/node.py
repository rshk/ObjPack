"""
The Node object
"""


class Node(object):
    object_name = None

    def __init__(self, *args, **kwargs):
        self.name = self.object_name or self.__class__.__name__
        self.attr = kwargs
        self.children = list(args)

    @classmethod
    def with_name(cls, *args, **kwargs):
        args = list(args)
        name = args.pop(0)
        obj = cls(*args, **kwargs)
        obj.name = name
        return obj

    def __repr__(self):
        return self.to_objpack()

    def to_objpack(self):
        contents = []
        for key, val in sorted(self.attr.iteritems()):
            contents.append('{0!s}={1!r}'.format(key, val))
        for val in self.children:
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


def create_node(name):
    class CustomNode(Node):
        pass
    CustomNode.object_name = name
    return CustomNode
