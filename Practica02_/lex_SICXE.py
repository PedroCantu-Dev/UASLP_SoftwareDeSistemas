from cmath import inf
from cmd import IDENTCHARS
import codecs
import ply.lex as lex
import ply.yacc as yacc
import re
import os
import sys
import math

# Valor de las banderas
# flags value
NIXBPE = ''
Nbit = 32
Ibit = 16
Xbit = 8
Bbit = 4
Pbit = 2
Ebit = 1

# Tabla de simbolos |
# Defined symbols                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           and their dir values
tabSym = {}

# codigo objeto
codOb = {}


# Contador de programa |
# Program counter
PC = 0

B = 0

# el diccionario retorna las expresiones regulares para cada token |
# This dictionary return regex for each token
# Descripcion de la notacion:
# las letras mayusculas se refierena los registros especificos
# 'm' indica una DIRECCION DE MEMORIA
# 'n' indica un ENTERO ENTRE 1 Y 16
# 'r1' 'r2' representan identificadores de registros
# los parentesis se usan para indicar el contenido de un registro o de una localidad de memoria
argumentTokens = {
    # tokens para instrucciones|
    # instructions tokens
    'operand': '''(@|#)?([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9]*)(,X)*''',
    # can be a character constant or a hexadecimal
    'm': '''([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9]*)''',
    'm,X': '''([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9]*),X''',
    'n': '''[0-9]+$''',  # "[0-9]|1[0-6]",
    'r': '''(A|X|L|B|S|T|F|PC|SW)''',

    # tokens para directivas|
    # addressing tokens
    'simbol': '''[a-zA-Z]+[a-zA-Z0-9]*''',
    '[simbol]': '''([a-zA-Z]+[a-zA-Z0-9]*)*''',  # con lo mismo que labels
    "C'TEXT'": '''(C|c)'[a-zA-Z0-9]*\'''',
    "X'HEX'": '''(X|x)'[0-9a-fA-F]+\'''',
    "dir": '''[0-9]+|[0-9a-fA-F]+H''',
    "val": '''[0-9]+|[0-9a-fA-F]+H''',
    "num": '''[0-9]+|[0-9a-fA-F]+H''',

    # tokens for operants
    'c': '''[0-9]+|[0-9a-fA-F]+H''',  # int or a hexadecimal
    'c,X': '''([0-9]+|[0-9a-fA-F]+H),X''',

    # tokens for new included expresions
    'EXP': '''[a-zA-Z]+[a-zA-Z0-9]*''',
}

arvhivoLex = {}

LexError = {}
SintaxError = {}

# Registros SICXE |
# SICXE Registers
SIXE_Registers = {'A': 0,  # Acumulador para operaciones aritmeticas |
                  'X': 1,  # Registro índice para direccionar |
                  'L': 2,  # Registro de enlace, para regreso de subrutinas |
                  'B': 3,  # Registro base para direccionamiento |
                  'S': 4,  # Registro de aplicacion general |
                  'T': 5,  # Registro de aplicacion general |
                  'F': 6,  # Acumulador de punto flotante |
                  'PC': 8,  # Contador de programa. Contiene la dirección de la siguiente instrucciona ejecutar |
                  'SW': 9}  # Palabra de estado, diversa información de banderas |


SICXE_Dictionary_Directives = {
    'START': ['D', 'START', 0],
    'END': ['D', 'END', 0],
    'BYTE': ['D', 'BYTE', -1],
    'WORD': ['D', 'WORD', 3],
    'RESB': ['D', 'RESB', -1],
    'RESW': ['D', 'RESW', -1],
    'BASE': ['D', 'BASE', 0],
}

SICXE_Dictionary_CodOp = {
    'ADD': ['I', 3, '0x18', ['operand']],
    'ADDF': ['I', 3, '0x58', ['operand']],
    'ADDR': ['I', 2, '0x90', ['r', 'r']],
    'AND': ['I', 3, '0x40', ['operand']],
    'CLEAR': ['I', 2, '0xB4', ['operand']],
    'COMP': ['I', 3, '0x28', ['operand']],
    'COMF': ['I', 3, '0x88', ['operand']],
    'COMPR': ['I', 2, '0xA0', ['r', 'r']],
    'DIV': ['I', 3, '0x24', ['operand']],
    'DIVF': ['I', 3, '0x64', ['operand']],
    'DIVR': ['I', 2, '0x9C', ['r', 'r']],
    'FIX': ['I', 1, '0xC4', ],
    'FLOAT': ['I', 1, '0xC0', ],
    'HIO': ['I', 1, '0xF4', ],
    'J': ['I', 3, '0x3C', ['operand']],
    'JEQ': ['I', 3, '0x30', ['operand']],
    'JGT': ['I', 3, '0x34', ['operand']],
    'JLT': ['I', 3, '0x38', ['operand']],
    'JSUB': ['I', 3, '0x48', ['operand']],
    'LDA': ['I', 3, '0x00', ['operand']],
    'LDB': ['I', 3, '0x68', ['operand']],
    'LDCH': ['I', 3, '0x50', ['operand']],
    'LDF': ['I', 3, '0x70', ['operand']],
    'LDL': ['I', 3, '0x08', ['operand']],
    'LDS': ['I', 3, '0x6C', ['operand']],
    'LDT': ['I', 3, '0x74', ['operand']],
    'LDX': ['I', 3, '0x04', ['operand']],
    'LPS': ['I', 3, '0xD0', ['operand']],
    'MUL': ['I', 3, '0x20', ['operand']],
    'MULF': ['I', 3, '0x60', ['operand']],
    'MULR': ['I', 2, '0x98', ['r', 'r']],
    'NORM': ['I', 1, '0xC8'],
    'OR': ['I', 3, '0x44', ['operand']],
    'RD': ['I', 3, '0xD8', ['operand']],
    'RMO': ['I', 2, '0xAC', ['r', 'r']],
    'RSUB': ['I', 3, '0x4C'],
    'SHIFTL': ['I', 2, '0xA4', ['r', 'n']],
    'SHIFTR': ['I', 2, '0xA8', ['r', 'n']],
    'SIO': ['I', 1, '0xF0'],
    'SSK': ['I', 3, '0xEC', ['operand']],
    'STA': ['I', 3, '0x0C', ['operand']],
    'STB': ['I', 3, '0x78', ['operand']],
    'STCH': ['I', 3, '0x54', ['operand']],
    'STF': ['I', 3, '0x80', ['operand']],
    'STI': ['I', 3, '0xD4', ['operand']],
    'STL': ['I', 3, '0x14', ['operand']],
    'STS': ['I', 3, '0x7C', ['operand']],
    'STSW': ['I', 3, '0xE8', ['operand']],
    'STT': ['I', 3, '0x84', ['operand']],
    'STX': ['I', 3, '0x10', ['operand']],
    'SUB': ['I', 3, '0x1C', ['operand']],
    'SUBF': ['I', 3, '0x5C', ['operand']],
    'SUBR': ['I', 2, '0x94', ['r', 'r']],
    'SVC': ['I', 2, '0xB0', ['n']],
    'TD': ['I', 3, '0xE0', ['operand']],
    'TIO': ['I', 1, '0xF8'],
    'TIX': ['I', 3, '0x2C', ['operand']],
    'TIXR': ['I', 2, '0xB8', ['r']],
    'WD': ['I', 3, '0xDC', ['operand']]}

# todas las reservadas concatenadas
SICXE_Dictionary = SICXE_Dictionary_CodOp | SICXE_Dictionary_Directives

tokens = [
    'NUM',
    'FINL',
    'COMA',
    'REG',
    'COMMENT_IL',
    'COMMENT_ML',
    'CODOP',
    'NAME',
    'DIRECTIV',
    'PLUS',
    'MODIF',
    'MINUS',
    'INT',
    'FLOAT_NUM',
    'HEX_INT',
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
    'OR_G',
    'AND_G',
    'FACTORIAL',
    'UMINUS',
    'OPERANDO',
    'C_TEXT',
    'X_HEX',
    'ARROBA',
    'NEWLINE'
]+list(SICXE_Dictionary.keys())

t_LPARENT = r'''\('''
t_RPARENT = r'''\)'''
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
t_OR_G = r'\|\|'
t_AND_G = r'\&\&'
t_EQUALS = r'\='
t_COMA = r'''\,'''
# t_OPERANDO = r'(\@|\#)?([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9]*)(\,X)*'
t_MODIF = r'''(\@|\#)'''


def t_COMMENT_ML(t):
    r'''\/\*[a-zA-Z0-9\s]+\*\/'''
    pass
    # t.type = 'COMMENT_ML'
    # return t


def t_newline(t):
    r'''\n+'''
    t.type = 'NEWLINE'
    t.lexer.lineno += len(t.value)
    return t


def t_C_TEXT(t):
    r"(C|c)\'[a-zA-Z0-9]*\'"
    t.type = 'C_TEXT'
    return t


def t_X_HEX(t):
    r"(X|x)\'[0-9a-fA-F]+\'"
    t.type = 'X_HEX'
    return t

# A NAME is a variable name. A variable can be 1 or more characters in length.
# The first character must be in the ranges a-z A-Z or be an underscore.
# Any character following the first character can be a-z A-Z 0-9 or an underscore.


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if(t.value in SICXE_Dictionary_CodOp):
        t.type = 'CODOP'
    elif(t.value in SICXE_Dictionary_Directives):
        # t.type = 'DIRECTIV'
        t.type = t.value
    elif(t.value in SIXE_Registers):
        t.type = 'REG'
    else:
        t.type = 'NAME'
    return t


# Ply's special t_ignore variable allows us to define characters the lexer will ignore.
# We're ignoring spaces.
t_ignore = ' \t'


def t_HEX_INT(t):
    r'\d+H'
    t.type = 'HEX_INT'
    return t


# More complicated tokens, such as tokens that are more than 1 character in length
# are defined using functions.
# A float is 1 or more numbers followed by a dot (.) followed by 1 or more numbers again.


def t_FLOAT_NUM(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# An int is 1 or more numbers.


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_COMMENT_IL(t):
    r'''[a-zA-Z0-9]+'''
    t.type = 'COMMENT_IL'
    return t

# Skip the current token and output 'Illegal characters' using the special Ply t_error function.


def t_error(t):
    print("Caracter ilegal en la linea " + str(lexer.lineno-1))
    # print("Illegal characters:"+t.value+":")
    t.lexer.skip(1)

 # Compute column.
 #     input is the input text string
 #     token is a token instance


def find_column(token):
    line_start = data.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


lexer = lex.lex()
# data = '''
# INICIO START 0H
# EJERCFINAL  START   0H
#             SIO
#             TIO
#             +LDX    @TABLA
# VALOR	    WORD    140
# 	   	    BASE    CAD
# TABLA  	    RESW	20
#     	    +LDS	VALOR, X
# 	   	    SHIFTL	S,6
# SIMBOLO     LDD		#VALOR
# 	        +LDA	1010H ,X
# CAD	        BYTE	C'FINAL'
# 	        LDA		#TABLA
#     	    SUBR	S, X
# 	   	    RESW	2500H
# SALTO       ADD		VALOR,X
# 	        STCH	@TABLA
# 	        JGT	    SALTO , X
# AREA        RESB	64
# 	        STA		SALTO
# 	        +SUB	350
# 	        J		CADENA, X
# 	        +TIX	TABLA,X
#             END     INICIO
# /*sdfsdflkjd\nsfASDFAFSD*/
# /*ComentarioPRRON*/
# &
# &


#  ADD ADDA ADDF ADDF_ _ADDF ADDFA ADDR ADDR_ AND
#  ANDA CLEAR _CLEAR UNOCLEAR DIV CLEARA CLEAR_ DIV
#  DIVIDENDO DIV
#  '''


data = '''
 EJERCFINAL  START   0H
             SIO\n
             TIO
             +LDX    @TABLA
             END     INICIO
 '''

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

print("fin lexer")


def p_programa(p):
    """programa : inicio proposiciones fin"""
    p[0] = ('programa', p[1], p[2], p[3])
    run(p[0])


def p_inicio(p):
    """inicio : etiqueta START numero COMMENT_IL NEWLINE
    | etiqueta START numero NEWLINE"""
    p[0] = (p[2], p[1], p[3])


def p_numero(p):
    """numero : INT
    | HEX_INT"""
    p[0] = ('numero', p[1])


def p_fin(p):
    """fin : END entrada """
    p[0] = ('END', p[2])


def p_entrada(p):
    """entrada : NAME"""
    {}


def p_proposiciones(p):
    """proposiciones : proposiciones proposicion
    | proposicion"""
    if(len(p) > 2):
        p[0] = str(p[1] + p[2])
    else:
        p[0] = str(p[1])


def p_proposicion(p):
    """proposicion : directiva COMMENT_IL NEWLINE
    | instruccion COMMENT_IL NEWLINE
    | directiva NEWLINE
    | instruccion NEWLINE"""
    {}


def p_instruccion(p):
    """
    instruccion : etiqueta opformato
    | opformato
    """
    {}


def p_directiva(p):
    """
    directiva : etiqueta tipodirectiva opdirectiva"""
    {}


def p_opdirectiva(p):
    """opdirectiva : NUM
    | NAME """
    {}


def p_tipodirectiva(p):
    """tipodirectiva : BYTE
    | WORD
    | RESB
    | RESW"""
    {}


def p_etiqueta(p):
    """etiqueta : NAME """
    p[0] = p[1]


def p_opformato(p):
    """opformato : f1
    | f2
    | f3
    | f4 """
    {}


def p_f3(p):
    """f3 : simple3
    | indirecto3
    | inmediato3
    | SIO
    | TIO"""
    p[0] = ('f3', p[1])


def p_f3_Indexado(p):
    """f3 : simple3 COMA 'X'
    | indirecto3 COMA 'X'
    | inmediato3 COMA 'X'"""
    p[0] = ('f3,X', p[1], p[2], p[3])


def p_f4(p):
    """f4 : PLUS f3"""
    p[0] = ('f4', p[1], p[2])


def p_simple3(p):
    """simple3 : CODOP NAME
    | CODOP NUM"""
    {}


def p_indirecto3(p):
    """indirecto3 : CODOP '@' NUM
    | CODOP '@' NAME"""
    {}


def p_inmediato3(p):
    """inmediato3 : CODOP '#' NUM
    | CODOP '#' NAME"""
    {}


def p_f2(p):
    """f2 : CODOP NUM
    | CODOP REG
    | CODOP REG COMA REG
    | CODOP REG COMA NUM"""
    {}


def p_f1(p):
    """f1 : CODOP NEWLINE"""
    {}


def p_empty(p):
    '''
    empty : NEWLINE
    '''
    p[0] = None


def p_error(p):
    print("syntax error")
    print(p)
    # p[0] = ("Err", p[1])


precedence = (
    ('left', 'NAME'),
    ('left', 'CODOP'),
    ('left', 'REG'),
    ('left', '@', '#'),
    ('left', 'OR_G', 'AND_G'),
    ('left', 'MORET', 'LESST', 'MOREEQ', 'LESSEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS', 'FACTORIAL')
)
parser = yacc.yacc()
env = {}


def des_hex(hexdigit):
    return int(hexdigit, 16)


def run(p):
    if type(p) == tuple:
        if(p[0] == 'programa'):
            return run(p[1]) + run(p[2]) + run(p[3])
        if p[0] == 'START':  # p[1]:etiqueta, p[2]:numero
            return run(p[1]) + str(run(p[2]))
        if p[0] == 'numero':
            {}
        if p[0] == 'BASE':
            {}
        if p[0] == 'DIRECTIV':
            {}
        if p[0] == 'f4':
            {}
        if p[0] == 'f3':
            {
                print("Hoola f3")
            }
        if p[0] == 'f2':
            {}
        if p[0] == 'f1':
            {}

        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            divisor = run(p[2])
            if(divisor > 0):
                return run(p[1]) / run(p[2])
            else:
                return inf
        elif p[0] == '%':
            return run(p[1]) % run(p[2])
        elif p[0] == '||':
            if(run(p[1]) > 0 or run(p[2]) > 0):
                return 1
            else:
                return 0
        elif p[0] == '&&':
            if(run(p[1]) > 0 and run(p[2]) > 0):
                return 1
            else:
                return 0
        elif p[0] == '<':
            if(run(p[1]) < run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '>':
            if(run(p[1]) > run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '<=':
            if(run(p[1]) <= run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '>=':
            if(run(p[1]) >= run(p[2])):
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
        print(p)
        return p


# while True:
#     try:
#         s = input('calc>> ')
#     except EOFError:
#         break
par = parser.parse(data)
# par = par = run(data)
print(par)

# while True:
#     try:
#         s = input('calc>> ')
#     except EOFError:
#         break
#     parser.parse(s)

# lexer.input(data)

# while True:
#     try:
#         s = input('lex-SICXE>>')
#         lexer.input(s)
#         while True:
#             try:
#                 tok = lexer.token()
#                 if not tok:
#                     break
#                 print(tok)
#             except:
#                 print("en corto")
#                 break
#     except EOFError:
#         break


#  # Give the lexer some input
#  lexer.input(data)

#  # Tokenize
#  while True:
#      tok = lexer.token()
#      if not tok:
#          break      # No more input
#      print(tok)
