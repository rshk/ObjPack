"""
Lexer for ObjPack format
"""

import re

import ply.lex as lex


tokens = (
    ## Comments (ignored)
    'COMMENT',

    ## Parenthesis, braces and brackets
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'LPAREN',
    'RPAREN',

    ## Fixed symbols
    'EQUAL',
    'COLON',
    'COMMA',

    ## Base types
    'STRING',
    'INTEGER',
    'FLOAT',
    'TRUE',
    'FALSE',
    'NULL',
    'SYMBOL',
)

## Whitespace gets ignored
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    raise TypeError("Unknown text {0!r}".format(t.value,))
    # t.lexer.skip(1)


def t_COMMENT(t):
    r'(\#|//).*'  # Both Python-style and JS-style comments
    return None  # Just skip this token


##------------------------------------------------------------
## Simple tokens
##------------------------------------------------------------

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUAL = r'='
t_COLON = r':'
t_COMMA = r','
t_SYMBOL = r'[a-zA-Z_][a-zA-Z0-9_]*'


##------------------------------------------------------------
## String tokenization
## Strings are in form: <flags>"<content>" (or single quotes)
##------------------------------------------------------------

simple_escape = r"""([a-zA-Z._~!=&\^\-\\?'"])"""
decimal_escape = r"""(\d+)"""
hex_escape = r"(x[0-9a-fA-F]+)"
escape_sequence = r"""(\\(""" + simple_escape + '|' + decimal_escape + '|' \
                  + hex_escape + '))'
string_flags = "[a-zA-Z]*"

# Double-quoted string
string_double_char = r"""([^"\\\n]|""" + escape_sequence + ')'
string_double = string_flags + '"' + string_double_char + '*"'

# Single-quoted string
string_single_char = r"([^'\\\n]|" + escape_sequence + ")"
string_single = string_flags + "'" + string_single_char + "*'"


@lex.TOKEN('|'.join((string_single, string_double)))
def t_STRING(t):
    ## Split "flags" prefix
    flags, string = re.match('^([a-zA-Z]*)(.*)$', t.value).groups()

    assert string[0] == string[-1]
    assert string[0] in ('"', "'")

    ## Token is a tuple with flags + raw string content
    t.value = (flags, string)
    return t


##------------------------------------------------------------
## Numbers tokenization
##------------------------------------------------------------

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


##------------------------------------------------------------
## Boolean/None
##------------------------------------------------------------

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
