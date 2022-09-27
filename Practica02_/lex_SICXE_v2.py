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
    # 'REG_X',
    'COMMENT_ML',
    'COMMENT_IL',
    'CODOP',
    'CODOP1',
    'CODOP2',  # por default será del tipo r1, r2 (CODOP_R_R)
    'CODOP2_R_N',
    'CODOP2_R',
    'CODOP2_N',
    'CODOP3',
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
    tDotValue = t.value
    if tDotValue in SICXE_Dictionary_Directives or tDotValue == 'RSUB':
        t.type = tDotValue
    elif tDotValue in SICXE_Dictionary_CodOp:
        if tDotValue == 'SHIFTL' or tDotValue == 'SHIFTR':
            t.type = 'CODOP2_R_N'
        elif tDotValue == 'TIXR' or tDotValue == 'CLEAR':
            t.type = 'CODOP2_R'
        else:
            t.type = 'CODOP' + str(SICXE_Dictionary_CodOp[tDotValue][1])
    elif(tDotValue in SIXE_Registers):
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
	        J		CADENA, X /*esto es un comentario


            como la vez*/
            +TIX	TABLA,X
            END     INICIO'''

lexer = lex.lex()
lexer.input(ejerFinal)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

###########################
# definicion del parser
#
##############################

precedence = (
    ('left', 'NEWLINE'),
    ('left', 'OR_G', 'AND_G'),
    ('left', 'MORET', 'LESST', 'MOREEQ', 'LESSEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS', 'EXTENDED', 'FACTORIAL'),
    ('right', 'AT', 'SHARP', 'EXTENDED'),
    ('right', 'NUM'),
    ('left', 'NAME'),
    ('left', 'CODOP'),
    ('left', 'REG'),
)


# opcional
start = 'sicxe_file'


def p_sicxe_file(p):
    """sicxe_file : programa
    | empty_nl programa
    | empty_nl programa empty_nl
    | programa empty_nl"""


def p_programa(p):
    """programa : inicio proposiciones fin"""
    p[0] = ('programa', p[1], p[2], p[3])


def p_inicio(p):
    """inicio : nombre_programa START int_type NEWLINE"""
    p[0] = ("inicio", p[1], p[2], p[3])


def p_nombre_programa(p):
    """nombre_programa : etiqueta"""


def p_fin(p):
    """fin : END entrada """
    p[0] = ('fin', p[1], p[2])


def p_entrada(p):
    """entrada : etiqueta"""


def p_proposiciones(p):
    """proposiciones : linea
    | proposiciones linea"""


def p_linea(p):
    """linea : f_column line_core il_comment NEWLINE"""


def p_first_column(p):
    """f_column : etiqueta
    | empty"""


def p_line_core(p):
    """line_core : instruccion
    | directiva"""

# c indica una constante entre 0 y 4095
# m indica una direccion de memoria o un valor mayor que 4095


def p_instruccion(p):
    """instruccion : f4
    | f3
    | f2
    | f1"""
    p[0] = p[1]


def p_f1(p):
    """f1 : CODOP1
    """

# nota: cuando se tiene un codop f2
# que requiera solo un registro , este se puede omitir
# y por default se le dara el valor 0


def p_f2(p):
    """f2 : CODOP2 REG COMA REG
    | CODOP2_R_N REG COMA INT
    | CODOP2_R REG
    | CODOP2_R
    """


def p_f2_error_(p):
    """f2 : CODOP2 error COMA REG
    | CODOP2 REG COMA error
    | CODOP2 error COMA error
    | CODOP2 error 
    | CODOP2_R_N REG COMA error
    | CODOP2_R_N error COMA INT"""


def p_f3(p):
    """f3 : CODOP3 simple3
    | CODOP3 indexado3
    | CODOP3 indirecto3
    | CODOP3 inmediato3
    | RSUB
    """


def p_f3_error_codop(p):
    """f3_error_codop : error simple3
    | error indexado3
    | error indirecto3
    | error inmediato3"""


def p_f3_error_operando(p):
    """f3_error_operando : CODOP3 error
    | RSUB error"""


def p_simple3(p):
    """simple3 : expression"""


def p_simple3_indexado3(p):
    """indexado3 : simple3 COMA REG"""


def p_indirecto3(p):
    """indirecto3 : AT expression"""


def p_inmediato3(p):
    """inmediato3 : SHARP expression"""


def p_f4(p):
    """f4 : PLUS f3 %prec EXTENDED"""
    p[0] = ('f4', p[1], p[2])


def p_directiva(p):
    """directiva : empty BYTE C_TEXT
    | empty BYTE X_HEX
    | empty WORD int_type
    | empty RESB int_type
    | BASE etiqueta
    """


def p_directiva_empty(p):
    """directiva :  BYTE empty C_TEXT
    | BYTE empty X_HEX
    | WORD empty int_type
    | RESB empty int_type
    | BASE empty etiqueta
    """


def p_int_type(p):
    """int_type : INT
    | HEX_INT
    """


def p_il_comment(p):
    """il_comment : COMMENT_IL
    | empty"""


def p_empty(p):
    """empty :
    | empty"""


def p_empty_nl(p):
    """ empty_nl : empty
    | NEWLINE
    | empty_nl"""


def p_empty_single_nl(p):
    """ empty_single_nl : empty
    | NEWLINE"""


def p_etiqueta(p):
    """etiqueta : NAME """
    p[0] = p[1]

##########################################
# La parte de la calculadora de expresiones
#
##########################################


def p_expression_uminus(p):
    '''expression : MINUS expression %prec UMINUS'''
    p[0] = -p[2]


def p_expression_uni(p):
    '''
    expression : FACTORIAL expression
    '''
    p[0] = (p[1], p[2])


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
               | expression OR_G expression
               | expression AND_G expression

    '''
    p[0] = (p[2], p[1], p[3])


def p_expression_assign(p):
    '''
    expression : NAME EQUALS expression
    '''
    p[0] = ('=', p[1], p[3])


def p_var_expression(p):
    '''
    var : NAME
    '''
    p[0] = ('var', p[1])


def p_expression_int_float_name(p):
    '''
    expression : INT
               | HEX_INT
               | var
    '''
    p[0] = p[1]


def p_expression_parent(p):
    '''
    expression : LPARENT expression RPARENT
    '''
    p[0] = p[2]


parser = yacc.yacc()
# par = parser.parse(input, debug=False)
