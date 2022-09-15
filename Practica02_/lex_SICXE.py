from cmd import IDENTCHARS
import codecs
import ply.lex as lex
import ply.yacc as yacc
import re
import os
import sys

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


# reservadas = {
#     'START': 'START',
#     'END': 'END',
#     'BYTE': 'BYTE',
#     'WORD': 'WORD',
#     'RESB': 'RESB',
#     'RESW': 'RESW',
#     'BASE': 'BASE',
#     'ADD': 'ADD',
#     'ADDF': 'ADDF',
#     'ADDR': 'ADDR',
#     'AND': 'AND',
#     'CLEAR': 'CLEAR',
#     'COMP': 'COMP',
#     'COMF': 'COMF',
#     'COMPR': 'COMPR',
#     'DIV': 'DIV',
#     'DIVF': 'DIVF',
#     'DIVR': 'DIVR',
#     'FIX': 'FIX',
#     'FLOAT': 'FLOAT',
#     'HIO': 'HIO',
#     'J': 'J',
#     'JEQ': 'JEQ',
#     'JGT': 'JGT',
#     'JLT': 'JLT',
#     'JSUB': 'JSUB',
#     'LDA': 'LDA',
#     'LDB': 'LDB',
#     'LDCH': 'LDCH',
#     'LDF': 'LDF',
#     'LDL': 'LDL',
#     'LDS': 'LDS',
#     'LDT': 'LDT',
#     'LDX': 'LDX',
#     'LPS': 'LPS',
#     'MUL': 'MUL',
#     'MULF': 'MULF',
#     'MULR': 'MULR',
#     'NORM': 'NORM',
#     'OR': 'OR',
#     'RD': 'RD',
#     'RMO': 'RMO',
#     'RSUB': 'RSUB',
#     'SHIFTL': 'SHIFTL',
#     'SHIFTR': 'SHIFTR',
#     'SIO': 'SIO',
#     'SSK': 'SSK',
#     'STA': 'STA',
#     'STB': 'STB',
#     'STCH': 'STCH',
#     'STF': 'STF',
#     'STI': 'STI',
#     'STL': 'STL',
#     'STS': 'STS',
#     'STSW': 'STSW',
#     'STT': 'STT',
#     'STX': 'STX',
#     'SUB': 'SUB',
#     'SUBF': 'SUBF',
#     'SUBR': 'SUBR',
#     'SVC': 'SVC',
#     'TD': 'TD',
#     'TIO': 'TIO',
#     'TIX': 'TIX',
#     'TIXR': 'TIXR',
#     'WD': 'WD',
# }

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
    # 'ID',
    'NUM',
    'FINL',
    'MODIF',
    'REGISTER',
    'COMMENT_IL',
    'CODOP',
    'ID',
    'INT',
    'FLOAT',
    'NAME'

]
# ] + list(SICXE_Dictionary.keys())
# ] + list(reservadas.values()) + list(SIXE_Registers.keys())

# t_ID = r'''[_]*[a-zA-Z]+[a-zA-Z0-9]*'''
# t_NUM = r'''[0-9]+|[0-9a-fA-F]+H'''
t_FINL = r'''\n'''
# t_MODIF = r'''(\@|\#)'''
t_COMMENT_IL = r'''[a-zA-Z0-9]+\n'''


def t_REGISTER(t):
    r'''( \sA\s |\sX\s | \sL\s | \sB\s | \sS\s | \sT\s | \sF\s | \sPC\s | \sSW\s )'''
    t.type = 'REGISTER'
    return t


def t_CODOP(t):
    r'''ADD |
      ADDF |
      ADDR |
      AND |
      CLEAR |
      COMP |
      COMF |
      COMPR |
     DIV |
      DIVF |
      DIVR |
      FIX |
      FLOAT |
     HIO |
      J |
      JEQ |
      JGT |
      JLT |
      JSUB |
      LDA |
      LDB |
      LDCH |
      LDF |
      LDL |
      LDS |
      LDT |
      LDX |
      LPS |
      MUL |
      MULF |
      MULR |
      NORM |
      OR |
      RD |
      RMO |
      RSUB |
      SHIFTL |
      SHIFTR |
      SIO |
      SSK |
      STA |
      STB |
      STCH |
      STF |
      STI |
      STL |
      STS |
      STSW |
      STT |
      STX |
      SUB |
      SUBF |
      SUBR |
      SVC |
      TD |
      TIO |
      TIX |
      TIXR |
      WD'''
    t.type = 'CODOP'
    return t


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


def t_error(t):
    print("Illegal characters:"+t.value+":")
    t.lexer.skip(1)


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


def p_programa():
    """programa : inicio proposiciones fin"""


def p_inicio():
    """inicio :
    etiqueta START NUM | proposicion"""


def p_fin():
    """"fin:
    END entrada | END entrada"""


def p_entrada():
    """entrada : ID | e"""


def p_proposiciones():
    """proposiciones : proposiciones proposicion | proposicion"""


# def p_comentario():
#     """comentario : COMMENT_IL | COMMENT_ML"""


def p_proposicion():
    """proposicion : instruccion COMMENT_IL | directiva COMMENT_IL | COMMENT_IL"""


def p_instruccion():
    """
    instruccion : etiqueta opformato
    """


def p_directiva():
    """
    directiva : etiqueta tipodirectiva opdirectiva"""


def opdirectiva():
    """opdirectiva : NUM | ID """


def p_tipodirectiva():
    """tipodirectiva : BYTE | WORD | RESB | RESW"""


def p_etiqueta():
    """etiqueta : ID """


def p_opformato():
    """opformato : f1 | f2  | f3 | f4 """


def p_f1():
    """f1 : CODOP"""


def p_f2():
    """f2 : CODOP NUM | CODOP REG | CODOP REG, REG | CODOP REG, NUM"""


def p_f3():
    """f3 : simple3 | indirecto3 | inmediato3"""


def p_f4():
    """f4 : +f3"""


def p_simple3():
    """simple3 : CODOP ID | CODOP NUM | CODOP NUM,X| CODOP ID,X"""


def p_indirecto3():
    """indirecto3 : CODOP @NUM | CODOP @ID"""


def p_inmediato3():
    """inmediato3 : CODOP #NUM | CODOP #ID"""


#    def p_codop():
#     """codop :  ADD |
#      ADDF |
#      ADDR |
#      AND |
#      CLEAR |
#      COMP |
#      COMF |
#      COMPR |
#      DIV |
#      DIVF |
#      DIVR |
#      FIX |
#      FLOAT |
#      HIO |
#      J |
#      JEQ |
#      JGT |
#      JLT |
#      JSUB |
#      LDA |
#      LDB |
#      LDCH |
#      LDF |
#      LDL |
#      LDS |
#      LDT |
#      LDX |
#      LPS |
#      MUL |
#      MULF |
#      MULR |
#      NORM |
#      OR |
#      RD |
#      RMO |
#      RSUB |
#      SHIFTL |
#      SHIFTR |
#      SIO |
#      SSK |
#      STA |
#      STB |
#      STCH |
#      STF |
#      STI |
#      STL |
#      STS |
#      STSW |
#      STT |
#      STX |
#      SUB |
#      SUBF |
#      SUBR |
#      SVC |
#      TD |
#      TIO |
#      TIX |
#      TIXR |
#      WD
#     """


# def t_OPERANDO(t):
#     return r'(@|#)?([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9]*)(,X)*'
# c indica una constante o dir de memoria entre 0 y 4095
# m indica una direccion de memoria o un valor constante mayor que 4095


# def p_sentence(p):
#     '''sentence : SIMBOL op
#     | SIMBOL op'''


# def p_constant(p):
#     '''constant_type : CONSTANT
#     | CONSTANT_H
#     '''


# def p_directiva(p):
#     '''
#     directiva : SIMBOLO START CONSTANT
#     | SIMBOLO START constant_type
#     | END SIMBOLO
#     | SIMBOLO BYTE C_TEXT
#     | SIMBOLO BYTE X_HEX
#     | SIMBOLO WORD constant_type
#     | SIMBOLO RESB constant_type
#     | SIMBOLO RESW constant_type
#     | SIMBOLO BASE SIMBOLO
#     '''


# el diccionario retorna las expresiones regulares para cada token |
# This dictionary return regex for each token
# Descripcion de la notacion:
# las letras mayusculas se refierena los registros especificos
# 'm' indica una DIRECCION DE MEMORIA
# 'n' indica un ENTERO ENTRE 1 Y 16
# 'r1' 'r2' representan identificadores de registros
# los parentesis se usan para indicar el contenido de un registro o de una localidad de memoria
# argumentTokens = {
#     # tokens para instrucciones|
#     # instructions tokens
#     'operand': "(@|#)?([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9]*)(,X)*",
#     # can be a character constant or a hexadecimal
#     'm': "([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9]*)",
#     'm,X': "([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9]*),X",
#     'n': "[0-9]+$",  # "[0-9]|1[0-6]",
#     'r': "(A|X|L|B|S|T|F|PC|SW)",

#     # tokens para directivas|
#     # addressing tokens
#     'simbol': "[a-zA-Z]+[a-zA-Z0-9]*",
#     '[simbol]': "([a-zA-Z]+[a-zA-Z0-9]*)*",  # con lo mismo que labels
#     "C'TEXT'": "(C|c)'[a-zA-Z0-9]*'",
#     "X'HEX'": "(X|x)'[0-9a-fA-F]+'",
#     "dir": "[0-9]+|[0-9a-fA-F]+H",
#     "val": "[0-9]+|[0-9a-fA-F]+H",
#     "num": "[0-9]+|[0-9a-fA-F]+H",

#     # tokens for operants
#     'c': "[0-9]+|[0-9a-fA-F]+H",  # int or a hexadecimal
#     'c,X': "([0-9]+|[0-9a-fA-F]+H),X",

#     # tokens for new included expresions
#     'EXP': '[a-zA-Z]+[a-zA-Z0-9]*',

# }
lexer = lex.lex()
data = '''SUM ADD 0 INICIO START 0H'''
lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)


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
