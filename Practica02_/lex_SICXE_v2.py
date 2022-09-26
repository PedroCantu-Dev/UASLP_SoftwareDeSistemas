from cmath import inf
from cmd import IDENTCHARS
import ply.lex as lex
import ply.yacc as yacc
import re
import math

# Tabla de simbolos |
# Defined symbols                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           and their dir values
tabSym = {}

# codigo objeto
codOb = {}

# Contador de programa |
# Program counter
PC = 0
B = -1

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

SICXE_Dictionary = SICXE_Dictionary_CodOp | SICXE_Dictionary_Directives

tokens = [
    'NUM',
    'FINL',
    'COMA',
    'REG',
    'COMMENT_ML',
    'COMMENT_IL',
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
    'NEWLINE',
    'AT',
    'SHARP',
    'EXTENDED'
]+list(SICXE_Dictionary.keys())

t_LPARENT = r'''\('''
t_RPARENT = r'''\)'''
t_PLUS = r'\+'
t_EXTENDED = r'\+'
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
t_AT = r'''\@'''
t_SHARP = r'''\#'''


def t_NEWLINE(t):
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
    if(t.value in SICXE_Dictionary_Directives or t.value == 'RSUB'):
        t.type = t.value
    elif(t.value in SICXE_Dictionary_CodOp):
        t.type = 'CODOP'
    elif(t.value in SIXE_Registers):
        t.type = 'REG'
    else:
        t.type = 'NAME'
    return t


def t_HEX_INT(t):
    r'\d+H'
    t.type = 'HEX_INT'
    return t

# An int is 1 or more numbers.


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# More complicated tokens, such as tokens that are more than 1 character in length
# are defined using functions.
# A float is 1 or more numbers followed by a dot (.) followed by 1 or more numbers again.


def t_FLOAT_NUM(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_COMMENT_ML(t):
    r'''\/\*[a-zA-Z0-9\s]+\*\/'''
    pass
    # t.type = 'COMMENT_ML'
    # return t


def t_COMMENT_IL(t):
    r'''[a-zA-Z0-9]+[\s]*'''
    pass
    # t.type = 'COMMENT_ML'
    # return t


# Skip the current token and output 'Illegal characters' using the special Ply t_error function.
# Ply's special t_ignore variable allows us to define characters the lexer will ignore.
# We're ignoring spaces.
t_ignore = ' \t'


def t_error(t):
    print("Caracter ilegal en la linea " +
          str(lexer.lineno-1) + " valor: " + t.value + "\n")
    # print("Illegal characters:"+t.value+":")
    t.lexer.skip(1)


ejerFinal = '''
 EJERCFINAL  START   0H
            SIO
            +LDX    @TABLA
VALOR	    WORD    140
	   	    BASE    CAD
TABLA  	    RESW	20
    	    +LDS	VALOR, X
	   	    SHIFTL	S,6
SIMBOLO     LDD		#VALOR
	        +LDA	1010H ,X
CAD	        BYTE	C'FINAL'
	        LDA		#TABLA
    	    SUBR	S, X
	   	    RESW	2500H
SALTO       ADD		VALOR,X
	        STCH	@TABLA
	        JGT	    SALTO , X
AREA        RESB	64
	        STA		SALTO
	        +SUB	350
	        J		CADENA, X
	        +TIX	TABLA,X
            END     INICIO'''

lexer = lex.lex()
lexer.input(ejerFinal)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)


def p_sicxe_file(p):
    """sicxe_file : programa
    | empty programa
    | empty programa empty
    | programa empty"""


def p_programa(p):
    """programa : inicio proposiciones fin"""
    p[0] = ('programa', p[1], p[2], p[3])


def p_inicio(p):
    """inicio : nombre_programa START numero NEWLINE"""
    p[0] = ("inicio", p[1], p[2], p[3])


def p_fin(p):
    """fin : END entrada """
    p[0] = ('fin', p[1], p[2])


def p_entrada(p):
    """entrada : """


def p_linea(p):
    """linea : f_column s_column t_column il_comment NEWLINE
    | inicio
    | fin"""


def p_first_column(p):
    """f_column : etiqueta"""


def p_second_column(p):
    """s_column : CODOP
    | tipodirectiva"""


def p_tipodirectiva(p):
    """tipodirectiva : BYTE
    | WORD
    | RESB
    | RESW
    | BASE"""
    p[0] = p[1]


def p_third_column(p):
    """t_column : expression"""


def p_il_comment(p):
    """il_comment : COMMENT_IL
    | empty"""


def empty(p):
    """empty : 
    | empty"""


def empty_nl(p):
    """ empty_nl : empty
    | NEWLINE
    | empty_nl"""


def empty_snl(p):
    """ empty_nl : empty
    | NEWLINE"""


def p_comment_il(p):
    """comment_il : 
    """
