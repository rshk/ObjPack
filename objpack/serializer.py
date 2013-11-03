import json
import io

# todo: we don't want to rely on json serialization for this..

_str_escape = {
    '"': '\"',
    "'": "\'",
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}


def _serialize_string(s):
    was_unicode = isinstance(s, unicode)
    if was_unicode:
        s = s.encode('utf-8')
    assert isinstance(s, bytes)
    output = io.BytesIO()
    for char in s:
        if char in _str_escape:
            output.write(_str_escape(char))
        else:
            ord_char = ord(char)
            if ord_char < 32 or ord_char > 127:
                output.write('\x{0:2X}'.format(ord_char))
            else:
                output.write()
        pass
    pass


def serialize(obj):
    ## Objects such as Node have a ``.to_objpack()`` method
    if hasattr(obj, 'to_objpack'):
        return obj.to_objpack()

    ## None, boolean and numbers are json-encoded
    if (obj is None) or (obj is True) or (obj is False) \
            or isinstance(obj, (int, long, float)):
        return json.dumps(obj).decode('utf-8')

    ## Unicode strings are first encoded
    if isinstance(obj, unicode):
        # todo: we don't want to rely on json serialization..
        return 'u' + json.dumps(obj.encode('utf-8')).decode('utf-8')

    ## Bytes strings are serialized using json
    if isinstance(obj, str):
        enc = io.BytesIO()
        enc.write('b"')
        for letter in obj:
            if letter == '"':
                enc.write('\"')
        enc.write('"')
        return enc.getvalue()

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
