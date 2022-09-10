import codecs
import ply.lex as lex
import re
import os
import sys

# SICXE_Dictionary = {
#              'START' : ['D','START',0],
#              'END'   : ['D','END',0],
#              'BYTE'  : ['D','BYTE',-1],
#              'WORD'  : ['D','WORD',3],
#              'RESB'  : ['D','RESB',-1],
#              'RESW'  : ['D','RESW',-1],
#              'BASE'  : ['D','BASE',0],
#              'ADD'   : ['I',3,'0x18',['operand']],
#              'ADDF'  : ['I',3,'0x58',['operand']],
#              'ADDR'  : ['I',2,'0x90',['r','r']],
#              'AND'   : ['I',3,'0x40',['operand']],
#              'CLEAR' : ['I',2,'0xB4',['operand']],
#              'COMP'  : ['I',3,'0x28',['operand']],
#              'COMF'  : ['I',3,'0x88',['operand']],
#              'COMPR' : ['I',2,'0xA0',['r','r']],
#              'DIV'   : ['I',3,'0x24',['operand']],
#              'DIVF'  : ['I',3,'0x64',['operand']],
#              'DIVR'  : ['I',2,'0x9C',['r','r']],
#              'FIX'   : ['I',1,'0xC4',],
#              'FLOAT' : ['I',1,'0xC0',],
#              'HIO'   : ['I',1,'0xF4',],
#              'J'     : ['I',3,'0x3C',['operand']],
#              'JEQ'   : ['I',3,'0x30',['operand']],
#              'JGT'   : ['I',3,'0x34',['operand']],
#              'JLT'   : ['I',3,'0x38',['operand']],
#              'JSUB'  : ['I',3,'0x48',['operand']],
#              'LDA'   : ['I',3,'0x00',['operand']],
#              'LDB'   : ['I',3,'0x68',['operand']],
#              'LDCH'  : ['I',3,'0x50',['operand']],
#              'LDF'   : ['I',3,'0x70',['operand']],
#              'LDL'   : ['I',3,'0x08',['operand']],
#              'LDS'   : ['I',3,'0x6C',['operand']],
#              'LDT'   : ['I',3,'0x74',['operand']],
#              'LDX'   : ['I',3,'0x04',['operand']],
#              'LPS'   : ['I',3,'0xD0',['operand']],
#              'MUL'   : ['I',3,'0x20',['operand']],
#              'MULF'  : ['I',3,'0x60',['operand']],
#              'MULR'  : ['I',2,'0x98',['r','r']],
#              'NORM'  : ['I',1,'0xC8'],
#              'OR'    : ['I',3,'0x44',['operand']],
#              'RD'    : ['I',3,'0xD8',['operand']],
#              'RMO'   : ['I',2,'0xAC',['r','r']],
#              'RSUB'  : ['I',3,'0x4C'],
#              'SHIFTL' : ['I',2,'0xA4',['r','n']],
#              'SHIFTR' : ['I',2,'0xA8',['r','n']],
#              'SIO'   : ['I',1,'0xF0'],
#              'SSK'   : ['I',3,'0xEC',['operand']],
#              'STA'   : ['I',3,'0x0C',['operand']],
#              'STB'   : ['I',3,'0x78',['operand']],
#              'STCH'  : ['I',3,'0x54',['operand']],
#              'STF'   : ['I',3,'0x80',['operand']],
#              'STI'   : ['I',3,'0xD4',['operand']],
#              'STL'   : ['I',3,'0x14',['operand']],
#              'STS'   : ['I',3,'0x7C',['operand']],
#              'STSW'  : ['I',3,'0xE8',['operand']],
#              'STT'   : ['I',3,'0x84',['operand']],
#              'STX'   : ['I',3,'0x10',['operand']],
#              'SUB'   : ['I',3,'0x1C',['operand']],
#              'SUBF'  : ['I',3,'0x5C',['operand']],
#              'SUBR'  : ['I',2,'0x94',['r','r']],
#              'SVC'   : ['I',2,'0xB0',['n']],
#              'TD'    : ['I',3,'0xE0',['operand']],
#              'TIO'   : ['I',1,'0xF8'],
#              'TIX'   : ['I',3,'0x2C',['operand']],
#              'TIXR'  : ['I',2,'0xB8',['r']],
#              'WD'   : ['I',3,'0xDC',['operand']]}

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
    'main': "MAIN",
    'START': 'START',
    'END': 'END',
    'BYTE': 'BYTE'
    'WORD': 'WORD'
    'RESB':
    'RESW':
    'BASE':
    'ADD':
    'ADDF':
    'ADDR':
    'AND':
    'CLEAR':
    'COMP':
    'COMF':
    'COMPR':
    'DIV':
    'DIVF':
    'DIVR':
    'FIX':
    'FLOAT':
    'HIO':
    'J':
    'JEQ':
    'JGT':
    'JLT':
    'JSUB':
    'LDA':
    'LDB':
    'LDCH':
    'LDF':
    'LDL':
    'LDS':
    'LDT':
    'LDX':
    'LPS':
    'MUL':
    'MULF':
    'MULR'
    'NORM'
    'OR',
    'RD',
    'RMO'
    'RSUB'
    'SHIFTL'
    'SHIFTR'

             'SIO'
    'SSK',
             'STA',
             'STB',
    'STCH',
    'STF',
    'STI',
    'STL',
    'STS',
    'STSW',
    'STT',
    'STX',
    'SUB',
    'SUBF',
    'SUBR'
    'SVC'
    'TD',
    'TIO'
    'TIX',
    'TIXR'
    'WD'
}

tokens = [
    'OPERANDO'

    'MSG',
    'ID',
    'CTE',
    'FLOAT',
    'PUNTOCOMA',
    'SBIZQ',
    'SBDER',
    'IGUAL',
    'COMA',
    'PARDER',
    'PARIZQ',
    'CBIZQ',
    'CBDER',
    'IGUALIGUAL',
    'DIFERENTE',
    'MAYOR',
    'MENOR',
    'MAYORQUE',
    'MENORQUE',
    'PLUS',
    'MENOS',
    'MULT',
    'DIV'
] + list(reservadas.values())


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
