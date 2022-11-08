import ply.lex as lex
import ply.yacc as yacc
import sys
import math

# Create a list to hold all of the token names
tokens = [

    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQUALS',
    'LPARENT',
    'RPARENT',
    'LESST',
    'MORET',
    'LESSEQ',
    'MOREEQ',
    'MOD',
    'OR',
    'AND',
    'FACTORIAL',
    'UMINUS'
]

# Use regular expressions to define what each token is
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_UMINUS = r'\-'
t_FACTORIAL = r'\!'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_MOD = r'\%'
t_LESST = r'\<'
t_MORET = r'\>'
t_LESSEQ = r'\<\='
t_MOREEQ = r'\>\='
t_OR = r'\|\|'
t_AND = r'\&\&'
t_EQUALS = r'\='


# Ply's special t_ignore variable allows us to define characters the lexer will ignore.
# We're ignoring spaces.
t_ignore = ' \t\n'


# More complicated tokens, such as tokens that are more than 1 character in length
# are defined using functions.
# A float is 1 or more numbers followed by a dot (.) followed by 1 or more numbers again.


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# An int is 1 or more numbers.


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# A NAME is a variable name. A variable can be 1 or more characters in length.
# The first character must be in the ranges a-z A-Z or be an underscore.
# Any character following the first character can be a-z A-Z 0-9 or an underscore.


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'NAME'
    return t

# Skip the current token and output 'Illegal characters' using the special Ply t_error function.


# def t_error(t):
#     print("Illegal characters:"+t.value+":")
#     t.lexer.skip(1)


# Build the lexer

lexer = lex.lex()


precedence = (
    ('left', 'OR', 'AND'),
    ('left', 'MORET', 'LESST', 'MOREEQ', 'LESSEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS', 'FACTORIAL')
)


# can be an expression or an empty
def p_calc(p):
    '''
    calc : expression
        | r_expression
        | a_expression
        | empty
    '''
    print(run(p[1].value))


def r_expression(p):
    '''
    r_expression : r_expression
    '''


def a_expression(p):


def p_expression_uminus(p):
    '''expression : MINUS expression %prec UMINUS'''
    p[0] = -p[2].value
    # p[0] = ('uminus', p[2])


def p_expression_uni(p):
    '''
    expression : FACTORIAL expression
    '''
    p[0] = (p[1].value, p[2].value)


def p_expression_bin(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression MULTIPLY expression
               | expression DIVIDE expression
               | expression MOD expression
               | expression LESST expression
               | expression MORET expression
               | expression LESSEQ expression
               | expression MOREEQ expression
               | expression OR expression
               | expression AND expression

    '''
    p[0] = (p[2].value, p[1].value, p[3].value)


def p_expression_assign(p):
    '''
    expression : NAME EQUALS expression
    '''
    p[0] = ('=', p[1].value, p[3].value)


def p_var_expression(p):
    '''
    var : NAME
    '''
    p[0] = ('var', p[1].value)


def p_expression_int_float_name(p):
    '''
    expression : INT
               | FLOAT
               | var
    '''
    p[0] = p[1].value


def p_expression_parent(p):
    '''
    expression : LPARENT expression RPARENT
    '''
    p[0] = p[2].value


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


def p_error(p):
    print("syntax error")
    print(p[0])


parser = yacc.yacc()
env = {}
# while True:
#     try:
#         s = input('calc>>')
#     except EOFError:
#         break
#     print(parser.parse(s))


def run(p):
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            divisor = run(p[2])
            if (divisor > 0):
                return run(p[1]) / run(p[2])
            else:
                return math.inf
        elif p[0] == '%':
            return run(p[1]) % run(p[2])
        elif p[0] == '||':
            if (run(p[1]) > 0 or run(p[2]) > 0):
                return 1
            else:
                return 0
        elif p[0] == '&&':
            if (run(p[1]) > 0 and run(p[2]) > 0):
                return 1
            else:
                return 0
        elif p[0] == '<':
            if (run(p[1]) < run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '>':
            if (run(p[1]) > run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '<=':
            if (run(p[1]) <= run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '>=':
            if (run(p[1]) >= run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '=':
            env[p[1]] = run(p[2])
            return env[p[1]]
        elif p[0] == 'uminus':
            print("funciono muminus")
            return -(run(p[1]))
        elif p[0] == 'var':
            return env[p[1]]
        elif p[0] == '!':
            return math.factorial(int(run(p[1])))
    else:
        # print(p)
        return p


while True:
    try:
        s = input('calc>> ')
    except EOFError:
        break
    parser.parse(s)


# Ensure our parser understands the correct order of operations.
# The precedence variable is a special Ply variable.
# precedence = (

#     ('left', 'PLUS', 'MINUS'),
#     ('left', 'MULTIPLY', 'DIVIDE')

# )

# Test it out
# data = '''
#  3 + 4 * 10
#    + -20 / 34 >=2 >(ssdR- 50) || 45<(89)*!76 <= 45
#  '''

# # Give the lexer some input
# lexer.input(data)

# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)
# try:
# s = input('>> ')

# except EOFError:
# break
# parser.parse(s)
