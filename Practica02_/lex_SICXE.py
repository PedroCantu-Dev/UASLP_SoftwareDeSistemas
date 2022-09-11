import codecs
import ply.lex as lex
import re
import os
import sys

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


reservadas = {
    'START': 'START',
    'END': 'END',
    'BYTE': 'BYTE',
    'WORD': 'WORD',
    'RESB': 'RESB',
    'RESW': 'RESW',
    'BASE': 'BASE',
    'ADD': 'ADD',
    'ADDF': 'ADDF',
    'ADDR': 'ADDR',
    'AND': 'AND',
    'CLEAR': 'CLEAR',
    'COMP': 'COMP',
    'COMF': 'COMF',
    'COMPR': 'COMPR',
    'DIV': 'DIV',
    'DIVF': 'DIVF',
    'DIVR': 'DIVR',
    'FIX': 'FIX',
    'FLOAT': 'FLOAT',
    'HIO': 'HIO',
    'J': 'J',
    'JEQ': 'JEQ',
    'JGT': 'JGT',
    'JLT': 'JLT',
    'JSUB': 'JSUB',
    'LDA': 'LDA',
    'LDB': 'LDB',
    'LDCH': 'LDCH',
    'LDF': 'LDF',
    'LDL': 'LDL',
    'LDS': 'LDS',
    'LDT': 'LDT',
    'LDX': 'LDX',
    'LPS': 'LPS',
    'MUL': 'MUL',
    'MULF': 'MULF',
    'MULR': 'MULR',
    'NORM': 'NORM',
    'OR': 'OR',
    'RD': 'RD',
    'RMO': 'RMO',
    'RSUB': 'RSUB',
    'SHIFTL': 'SHIFTL',
    'SHIFTR': 'SHIFTR',
    'SIO': 'SIO',
    'SSK': 'SSK',
    'STA': 'STA',
    'STB': 'STB',
    'STCH': 'STCH',
    'STF': 'STF',
    'STI': 'STI',
    'STL': 'STL',
    'STS': 'STS',
    'STSW': 'STSW',
    'STT': 'STT',
    'STX': 'STX',
    'SUB': 'SUB',
    'SUBF': 'SUBF',
    'SUBR': 'SUBR',
    'SVC': 'SVC',
    'TD': 'TD',
    'TIO': 'TIO',
    'TIX': 'TIX',
    'TIXR': 'TIXR',
    'WD': 'WD',
}

tokens = [
    'DIR_MODIFIER',  # @ --> Indirecto.  # --> inmediato.
    'CONSTANT',
    'CONSTANT_H',
    'C_TEXT',
    'X_HEX',
    'SIMBOL'


] + list(reservadas.values())
# ] + list(reservadas.values()) + list(SIXE_Registers.keys())

t_DIR_MODIFIER = r'''(A|X|L|B|S|T|F|PC|SW)'''


def t_OPERANDO(t):
    return r'(@|#)?([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9]*)(,X)*'
# c indica una constante o dir de memoria entre 0 y 4095
# m indica una direccion de memoria o un valor constante mayor que 4095


def p_sentence(p):
    '''sentence : SIMBOL op
    | SIMBOL op'''


def p_constant(p):
    '''constant_type : CONSTANT
    | CONSTANT_H
    '''


def p_directiva(p):
    '''
    directiva : SIMBOLO START CONSTANT
    | SIMBOLO START constant_type
    | END SIMBOLO
    | SIMBOLO BYTE C_TEXT
    | SIMBOLO BYTE X_HEX
    | SIMBOLO WORD constant_type
    | SIMBOLO RESB constant_type
    | SIMBOLO RESW constant_type 
    | SIMBOLO BASE SIMBOLO
    '''


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
    'operand': "(@|#)?([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9]*)(,X)*",
    # can be a character constant or a hexadecimal
    'm': "([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9]*)",
    'm,X': "([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9]*),X",
    'n': "[0-9]+$",  # "[0-9]|1[0-6]",
    'r': "(A|X|L|B|S|T|F|PC|SW)",

    # tokens para directivas|
    # addressing tokens
    'simbol': "[a-zA-Z]+[a-zA-Z0-9]*",
    '[simbol]': "([a-zA-Z]+[a-zA-Z0-9]*)*",  # con lo mismo que labels
    "C'TEXT'": "(C|c)'[a-zA-Z0-9]*'",
    "X'HEX'": "(X|x)'[0-9a-fA-F]+'",
    "dir": "[0-9]+|[0-9a-fA-F]+H",
    "val": "[0-9]+|[0-9a-fA-F]+H",
    "num": "[0-9]+|[0-9a-fA-F]+H",

    # tokens for operants
    'c': "[0-9]+|[0-9a-fA-F]+H",  # int or a hexadecimal
    'c,X': "([0-9]+|[0-9a-fA-F]+H),X",

    # tokens for new included expresions
    'EXP': '[a-zA-Z]+[a-zA-Z0-9]*',

}


t_MSG = r'\".+\"'
t_PLUS = r'\+'
t_IGUAL = r'\='
t_MENOS = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'
t_PUNTOCOMA = r'\;'
t_SBIZQ = r'\['
t_SBDER = r'\]'
t_COMA = r'\,'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CBIZQ = r'\{'
t_CBDER = r'\}'
t_IGUALIGUAL = r'\=='
t_DIFERENTE = r'\!='
t_MAYOR = r'\>'
t_MENOR = r'\<'
t_MAYORQUE = r'\>='
t_MENORQUE = r'\<='


t_ignore = ' \t'


def t_ID(t):
    r'[a-zA-Z_]+[a-zA-Z0-9]*'
    if t.value.upper() in reservadas.values():
        t.value = t.value.upper()
        t.type = t.value
    return t


def t_ignore_COMMENT(t):
    r'\#.+'
    pass


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_CTE(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_error(t):
    print("ILLEGAL CHARACTER %s" % t.value[0])
    t.lexer.sikip[1]


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


lexer = lex.lex()
