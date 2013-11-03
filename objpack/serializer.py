import json
import io
import sys

# todo: we don't want to rely on json serialization for this..

PY3K = sys.version_info[0] == 3

_str_escape = {
    '"': '\"',
    "'": "\'",
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}

if PY3K:
    numeric_types = (int, float)
else:
    numeric_types = (int, long, float)


def _serialize_string(s):
    if isinstance(s, unicode):
        s = s.encode('utf-8')
    assert isinstance(s, bytes)

    output = io.BytesIO()
    for char in s:
        if isinstance(char, int):  # Py3k w/ bytes
            char, ord_char = chr(char), char
        else:
            ord_char = ord(char)

        if char in _str_escape:
            output.write(_str_escape[char])
        elif ord_char < 32 or ord_char > 127:
            output.write('\\x{0:2X}'.format(ord_char))
        else:
            output.write(char.encode('utf-8'))
    out = output.getvalue()
    return out


def serialize(obj):
    ## Objects such as Node have a ``.to_objpack()`` method
    if hasattr(obj, 'to_objpack'):
        return obj.to_objpack()

    ## None, boolean and numbers are json-encoded
    if (obj is None) or (obj is True) or (obj is False) \
            or isinstance(obj, numeric_types):
        return json.dumps(obj)

    ## Unicode strings are first encoded
    if isinstance(obj, unicode):
        # Note: we omit the 'u' flag to be json-compatible.
        return '"{0}"'.format(_serialize_string(obj.encode('utf-8')))

    ## Bytes strings are serialized using json
    if isinstance(obj, str):
        return 'b"{0}"'.format(_serialize_string(obj))

    ## Lists and tuples become lists
    if isinstance(obj, (tuple, list)):
        return '[{0}]'.format(','.join(serialize(o) for o in obj))

    ## Dictionaries
    if isinstance(obj, dict):
        return '{{{0}}}'.format(
            ','.join(
                '{0}:{1}'.format(serialize(k), serialize(v))
                for k, v in obj.iteritems()))

    ## Unknown objects :(
    raise ValueError("Unserializable object: {0!r}".format(obj))
