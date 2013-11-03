import io

import ply.yacc as yacc

from .lexer import tokens
from .node import Node


def p_expression(p):
    """
    expression : dict
               | list
               | object
               | string
               | FLOAT
               | INTEGER
               | TRUE
               | FALSE
               | NULL
    """
    p[0] = p[1]


## Strings
##------------------------------------------------------------

def p_string(p):
    """
    string : unified_string
    """
    # todo: here we need to recompose string properly

    # Each item of unified_string is a (flags, string)
    # tuple. We need to merge all of them.

    # String flags are as follows:

    # b - binary string
    # u - unicode string (default)
    # r - raw string (do not process escapes)
    # B - base64 encoded
    # H - hex encoded string

    ## In this first implementation we enforce flags
    ## to be the same or to be absent on subsequent
    ## parts.

    parts = p[1]

    for flags, string in parts[1:]:
        if flags and (flags != parts[0][0]):
            ## Flags are not empty and differ from
            ## flags of the first piece
            raise ValueError("Mismatching flags")

    charset = None
    encoding = None
    raw = False
    flags = parts[0][0]

    for flag in flags:
        if flag in 'ub':
            if charset is not None:
                raise ValueError("Multiple flags: 'ub'")
            charset = flag
        elif flag in 'BH':
            if encoding is not None:
                raise ValueError("Multiple flags: 'BH'")
            encoding = flag
        elif flag == 'r':
            raw = True
        # todo: else: -> what??

    if charset is None:
        charset = 'u'

    def decode(part):
        s = part[1:-1]

        if charset == 'u':
            if isinstance(s, bytes):
                s = unicode(s, encoding='utf-8')
        else:
            if isinstance(s, unicode):
                s = s.encode('utf-8')

        if not raw:
            # Apply escape replacements
            output = io.BytesIO() if charset == 'b' else io.StringIO()
            si = iter(s)
            for char in si:
                if char == '\\':
                    nxchar = si.next()
                    if nxchar == 'n':
                        output.write('\n' if charset == 'b' else u'\n')
                    elif nxchar == 'r':
                        output.write('\r' if charset == 'b' else u'\r')
                    elif nxchar == 't':
                        output.write('\t' if charset == 'b' else u'\t')
                    elif nxchar == 'b':
                        output.write('\b' if charset == 'b' else u'\b')
                    elif nxchar == 'f':
                        output.write('\f' if charset == 'b' else u'\f')
                    # todo: \0###, \x## and \u#### escapes
                    else:
                        output.write(nxchar)
                else:
                    output.write(char)
            s = output.getvalue()

        return s

    glue = '' if charset == 'b' else u''
    p[0] = glue.join(decode(x[1]) for x in parts)


def p_unified_string(p):
    """unified_string : STRING"""
    p[0] = [p[1]]


def p_unified_string_2(p):
    """unified_string : unified_string STRING"""
    p[0] = p[1] or []
    p[0].append(p[2])


## Dictionaries
##------------------------------------------------------------

def p_dict(p):
    """
    dict : LBRACE dict_content RBRACE
         | LBRACE dict_content COMMA RBRACE
    """
    p[0] = dict(p[2] or [])


def p_dict_content_empty(p):
    "dict_content :"
    p[0] = []


def p_dict_content(p):
    """
    dict_content : dict_keyval
                 | dict_content COMMA dict_keyval
    """
    if len(p) == 1:
        p[0] = []

    elif len(p) == 2:
        p[0] = [p[1]]

    elif len(p) == 4:
        p[0] = p[1] or []
        p[0].append(p[3])


def p_dict_keyval(p):
    """
    dict_keyval : string COLON expression
                | INTEGER COLON expression
                | FLOAT COLON expression
    """
    p[0] = (p[1], p[3])


def p_list(p):
    """
    list : LBRACKET RBRACKET
         | LBRACKET list_content RBRACKET
         | LBRACKET list_content COMMA RBRACKET
    """
    if len(p) == 3:  # Empty list
        p[0] = []
    else:  # We have some content
        p[0] = p[2]


def p_list_content(p):
    """
    list_content : expression
                 | list_content COMMA expression
    """
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] or []
        p[0].append(p[3])
    else:
        assert False, "Internal error"


def p_object(p):
    """
    object : SYMBOL LPAREN RPAREN
           | SYMBOL LPAREN object_content RPAREN
           | SYMBOL LPAREN object_content COMMA RPAREN
    """
    p[0] = Node.with_name(p[1])

    if len(p) >= 5:
        # We have some content too..
        for typ, val in p[3]:
            if typ == 'attr':
                p[0].attr[val[0]] = val[1]
            elif typ == 'child':
                p[0].children.append(val)
            else:
                assert False, "Internal error"


def p_object_content(p):
    """
    object_content : object_content_item
                   | object_content COMMA object_content_item
    """
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] or []
        p[0].append(p[3])
    else:
        raise TypeError()


def p_object_content_item(p):
    """
    object_content_item : object_content_attr
                        | object_content_child
    """
    p[0] = p[1]


def p_object_content_child(p):
    """
    object_content_child : expression
    """
    p[0] = ('child', p[1])


def p_object_content_attr(p):
    """
    object_content_attr : SYMBOL EQUAL expression
    """
    p[0] = ('attr', (p[1], p[3]))


def p_error(p):
    raise TypeError("Parser error! {0!r}".format(p))


parser = yacc.yacc()
