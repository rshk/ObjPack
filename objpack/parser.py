from ply import lex, yacc

from .node import Node


## Lexer rules
##============================================================

tokens = (
    'COMMENT',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'LPAREN',
    'RPAREN',
    'EQUAL',
    'STRING',
    'COLON',
    'COMMA',
    'FLOAT',
    'INTEGER',
    'TRUE',
    'FALSE',
    'NULL',
    'SYMBOL',
)

t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    raise TypeError("Unknown text {0!r}".format(t.value,))
    # t.lexer.skip(1)


def t_COMMENT(t):
    r'\#.*'
    return None  # Skip token


t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUAL = r'='

#string_single = r"'([^']|\')*'"
#string_double = r'"([^"]|\")*"'

simple_escape = r"""([a-zA-Z._~!=&\^\-\\?'"])"""
decimal_escape = r"""(\d+)"""
hex_escape = r"(x[0-9a-fA-F]+)"
escape_sequence = r"""(\\(""" + simple_escape + '|' + decimal_escape + '|' \
                  + hex_escape + '))'

# string literals (K&R2: A.2.6)
string_double_char = r"""([^"\\\n]|""" + escape_sequence + ')'
string_double = '"' + string_double_char + '*"'
string_single_char = r"([^'\\\n]|" + escape_sequence + ")"
string_single = "'" + string_single_char + "*'"


@lex.TOKEN('|'.join((string_single, string_double)))
def t_STRING(t):
    assert t.value[0] == t.value[-1]
    delimiter = t.value[0]
    if delimiter in ('"', "'"):
        t.value = t.value[1:-1]
        t.value = t.value.replace('\\' + delimiter, delimiter)
        # todo: process escape characters..
        # todo: we might want to consider unicode/bytes/raw strings, ...?
    else:
        assert False, "Should never get here!"
    return t


t_COLON = r':'
t_COMMA = r','
t_SYMBOL = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_TRUE(t):
    r'true'
    t.value = True
    return t


def t_FALSE(t):
    r'false'
    t.value = False
    return t


def t_NULL(t):
    r'null'
    t.value = None
    return t


lexer = lex.lex()


## Parser rules
##============================================================

def p_expression(p):
    """
    expression : dict
               | list
               | object
               | unified_string
               | FLOAT
               | INTEGER
               | TRUE
               | FALSE
               | NULL
    """
    p[0] = p[1]


def p_unified_string(p):
    """
    unified_string : STRING
                   | unified_string STRING
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]


def p_dict(p):
    """
    dict : LBRACE RBRACE
         | LBRACE dict_content RBRACE
         | LBRACE dict_content COMMA RBRACE
    """
    if len(p) == 3:
        # Empty dict
        p[0] = {}
    else:
        # We have some content
        p[0] = dict(p[2] or [])


def p_dict_content(p):
    """
    dict_content : dict_keyval
                 | dict_content COMMA dict_keyval
    """
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] or []
        p[0].append(p[3])


def p_dict_keyval(p):
    """
    dict_keyval : STRING COLON expression
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
    p[0] = Node(p[1])

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
