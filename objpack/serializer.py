import json
import io
import sys

import six

# todo: we don't want to rely on json serialization for this..

numeric_types = six.integer_types + (float,)

_str_escape = {
    '"': u'\"',
    "'": u"\'",
    '\b': u'\\b',
    '\f': u'\\f',
    '\n': u'\\n',
    '\r': u'\\r',
    '\t': u'\\t',
}


def _serialize_bytes(s):
    """Serialize a "bytes" string

    :param s:
        the bytes string to be encoded
    :return:
        a unicode string containing the serialized string
    """
    # todo: if we have many non-printable characters, we
    # can decide to base64-encode the thing..
    # In this case, we add the B flag.
    assert isinstance(s, six.binary_type)
    output = six.StringIO()
    # We just want to encode non-printable characters
    # todo: use "special" codes when possible..
    for char in six.iterbytes(s):
        ch = six.int2byte(char)  # The actual character
        if ch in _str_escape:
            output.write(_str_escape[ch])
        elif 32 >= char <= 126:
            output.write(u'\\x{0:02X}'.format(char))
        else:
            output.write(ch.decode('utf-8'))
    return u'b"{0}"'.format(output.getvalue())


def _serialize_string(s):
    assert isinstance(s, six.text_type)
    output = six.StringIO()

    for char in s:
        ord_char = ord(char)

        if char in _str_escape:
            output.write(_str_escape[char])

        elif ord_char < 32 or ord_char > 127:
            # todo: we need to handle unicode properly!!
            # how to escape non-printable unicode characters?
            # find all the prefix + encode?
            # but, we might want to preserve characters as well..
            output.write('\\x{0:2X}'.format(ord_char))

        else:
            output.write(char)

    # Note: we omit the 'u' flag to be json-compatible.
    return u'"{0}"'.format(output.getvalue())


def serialize(obj):
    ## Objects such as Node have a ``.to_objpack()`` method
    if hasattr(obj, 'to_objpack'):
        return obj.to_objpack()

    ## None, boolean and numbers are json-encoded
    if (obj is None) or (obj is True) or (obj is False) \
            or isinstance(obj, numeric_types):
        return json.dumps(obj)

    ## Unicode strings are first encoded
    if isinstance(obj, six.text_type):
        return _serialize_string(obj)

    ## Bytes strings are serialized using json
    if isinstance(obj, six.binary_type):
        return _serialize_bytes(obj)

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
