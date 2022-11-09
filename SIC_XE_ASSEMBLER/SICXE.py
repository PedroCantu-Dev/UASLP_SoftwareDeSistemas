# ERRORES|EERRORS
# Mnemonico no encontrado |
# No Mnemonic
# Uso duplicado de etiqueta |
# Using the same label twice
# Etiqueta indefinida |
# Undefined labels
# Error de sintaxis |
# syntax error
# Error de direccionamiento |
# Addressing Mode Errors
# direccionamiento relativo en formato 3 |
# Relative addressing impossible on format 3.
from math import *
import re
from string import hexdigits
import string
from typing import Iterable  # for regular expresions
import calc.calc as calc


# Diccionario de directivas y nemonicos |
# mnemonics and adressing modes dictioanary
SICXE_Dictionary = {
    'START': ['D', 'START', 0],
    'END': ['D', 'END', 0],
    'BYTE': ['D', 'BYTE', -1],
    'WORD': ['D', 'WORD', 3],
    'RESB': ['D', 'RESB', -1],
    'RESW': ['D', 'RESW', -1],
    'BASE': ['D', 'BASE', 0],
    # las directivas añadidas para los nuevos features
    'EQU': ['D', 'EQU', 0],
    'USE': ['D', 'USE', 0],
    'ORG': ['D', 'ORG', 0],
    # directivas para secciones de control
    'CSECT': ['D', 'CSECT', 0],
    'EXTDEF': ['D', 'EXTDEF', 0],
    'EXTREF': ['D', 'EXTREF', 0],
    # todas las instrucciones
    'ADD': ['I', 3, '0x18', ['operand']],
    'ADDF': ['I', 3, '0x58', ['operand']],
    'ADDR': ['I', 2, '0x90', ['r', 'r']],
    'AND': ['I', 3, '0x40', ['operand']],
    'CLEAR': ['I', 2, '0xB4', ['r']],
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

# c indica una constante o dir de memoria entre 0 y 4095
# m indica una direccion de memoria o un valor constante mayor que 4095
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


def xor(x, y):
    return bool((x and not y) or (not x and y))


def getFineOperand(arrayOfPossibleOperands):
    if (len(arrayOfPossibleOperands) == 1):  # if the operand is unique there is nothing to do
        return arrayOfPossibleOperands[0]
    elif (len(arrayOfPossibleOperands) == 2):
        # it means the next operand is part of the ecuation
        if (xor(arrayOfPossibleOperands[0][-1] == ',',  arrayOfPossibleOperands[1][0] == ',')):
            return arrayOfPossibleOperands[0] + arrayOfPossibleOperands[1]
        else:
            return arrayOfPossibleOperands[0]
    elif (len(arrayOfPossibleOperands) >= 3):
        if (arrayOfPossibleOperands[1] == ','):
            return arrayOfPossibleOperands[0] + arrayOfPossibleOperands[1] + arrayOfPossibleOperands[2]
        # it means the next operand is part of the ecuation
        elif (xor(',' == arrayOfPossibleOperands[0][-1], ',' == arrayOfPossibleOperands[1][0])):
            return arrayOfPossibleOperands[0] + arrayOfPossibleOperands[1]
        else:
            return arrayOfPossibleOperands[0]


# Optab = {}
# Optab2 = {}

symbolsTables = {}
blocksTables = {}


X = 0

isBase = False
BaseLoc = 0
Flags = 0


def isExtended(mnemonic):
    if (mnemonic == baseMnemonic(mnemonic)):
        return None
    else:
        return 1

# dice si una instruccion es tipo 4


def typeFour(mnemonic):
    if mnemonic[0] == "+":
        return 1
    return None

# dice si una instruccion es tipo 4


def typeSIC(mnemonic):
    if mnemonic in ("FIX" or "FLOAT" or "HIO" or "SIO" or "TIO"):
        return 1
    return None


def isString(operands):
    return operands[0] == 'C'


def isspace(line):
    return False


def isSymbol(string):
    return string in tabSym.keys()

# Regresa el nemonico como tal, sin signo + |
# Return the mnemonic strin with any leading + striped off


def baseMnemonic(mnemonic):
    if mnemonic[0] == "+":
        return mnemonic[1:]
    return mnemonic

# retorna el operando sin tipo de direccionamiento


def baseOperand(operand):
    res = operand
    if res[0] == "@" or res[0] == "#":
        res = operand[1:]
    if (res.endswith(',X')):
        res = res.replace(',X', '')
    return res

# Retorna 1 si el primer caracter es diferente a espacios lo que quiere decir que hay una etiqueta|
# Return 1 if the first character is different to any type of space, that means it is a label


def haslabel(c):
    return c != ' ' and c != '\t' and c != '\n'

# Retorna 1 si la linea omienza con un punto |
# return 1 if the line begin with point.


def isComment(c):
    return c == '?'

# analisis gramatical | parser


def parseLine(line):

    # Si la linea empieza con punto la toma como comentario |
    # If the line begins with a point it is a comment
    if isComment(line[0]):
        return ['', '', '', line]

    label = ''
    mnemonic = ''
    operands = ''

    findComment = line.find("?")
    if (findComment >= 0):
        comment = line[findComment:-1]
        line = line[0:findComment]

    # Split the words of the line
    lineWords = line.split()

    if baseMnemonic(lineWords[0]) in SICXE_Dictionary:
        mnemonic = lineWords[0]
        if len(lineWords) >= 2:  # if has operands
            operands = getFineOperand(lineWords[1:])  # lineWords[1]
    else:
        if haslabel(line[0]):  # has labels at the begining of the line
            label = lineWords[0]
            mnemonic = lineWords[1]
            if len(lineWords) >= 3:  # if has one or more operands
                operands = getFineOperand(lineWords[2:])  # lineWords[2]
        else:
            mnemonic = lineWords[0]
            if len(lineWords) >= 2:  # if has operands
                operands = getFineOperand(lineWords[1:])  # lineWords[1]
    return (label, mnemonic, operands, '')

# function to return key for any value


def get_key(val: object, my_dict: dict):
    for key, value in my_dict.items():
        if val == value:
            return key
    return "key doesn't exist"

# determina si una direccion es relativa a la base, esta tiene que ser hexadecimal |
# determine if a given address is relative to the base, the address must be in hexadecimal


def addressIsBaseRelative(hexAddress):
    if int(hexAddress, 16) >= 0 and int(hexAddress, 16) <= 4096:
        return True
    else:
        return False

# determina si una direccion es relativa al contador de programa, esta tiene que ser hexadecimal |
# determine if a given address is relative to program counter, the address must be in hexadecimal


def addressIsPCRelative(hexAddress):
    if int(hexAddress, 16) >= -2048 and int(hexAddress, 16) <= 2047:
        return True
    else:
        return False

# return True if the range of the costant is between 0 and 4095


def argumentIsA_c_Constant(argument):
    if (int(argument, 16) >= 0 and int(argument, 16) <= 4095):
        return True
    else:
        return False

# return True if the range of the costant is between grader than 4095


def argumentIsA_m_Constant(argument):
    if (int(argument, 16) > 4095):
        return True
    else:
        return False


def instruLen(instru):
    instruDefArray = SICXE_Dictionary.get(baseMnemonic(instru))
    if (instruDefArray[1] == 3):
        if (typeFour(instru)):
            return 0x04
        else:
            return 0x03
    elif (instruDefArray[1] == 2):
        return 0x02
    else:
        return 0x01

# determina si el numero de carateres hexadecimales es par o impar para completar los bytes


def padHexEven(string):
    if (len(string) % 2):
        return '0'+string
    return string

# this function extracts the substring between markers


def byteOperandExtract(raw_string):
    start_marker = "'"
    end_marker = "'"
    start = raw_string.index(start_marker) + len(start_marker)
    end = raw_string.index(end_marker, start)
    return raw_string[start:end]

# retorna la cantidad de bytes necesarios segun la directiva |
# return the number of bytes needed deppending of the directive


def directiveLen(directive, operand):
    directiveDefArray = SICXE_Dictionary.get(baseMnemonic(directive))
    res = 0x00
    # BYTE C'Texto' or X'025A'
    if (directiveDefArray[1] == 'BYTE'):  # for byte directive
        strExtract = byteOperandExtract(operand)
        if (operand.startswith('c'.upper())):
            res = len(strExtract)
        elif (operand.startswith('x'.upper())):
            # divided by two becuse each byte uses two nibbles
            res = int(len(padHexEven(strExtract))/2)
    # WORD Valor. El valor puede expresarse en decimal o hexadecimal.
    # genera una constante entera de una palabra(3 bytes)
    elif (directiveDefArray[1] == 'WORD'):
        res = 0x03
    # RESB Número. el numero puede expresarse en decimal o hexadecimal.
    elif (directiveDefArray[1] == 'RESB'):  # reseva el numero de bytes indicado
        res = getHexadecimalByString(operand)
    # RESW Número. Numero puede ser decimal o hexadecimal
    # indica el numero de palabras a reservar
    elif (directiveDefArray[1] == 'RESW'):
        res = 3 * getHexadecimalByString(operand)
    return res

# converts any decimal or hexadecimal string into a hexadecimal value


# at this point the lexical analyzer made its work so, it suóse there is not error whenhex parsing
def getHexadecimalByString(strConvert):
    res = None
    if (strConvert.isdecimal()):
        res = int(strConvert)
    elif (correctHex(strConvert)):
        res = int(strConvert.replace("h".upper(), ""), 16)
    return res


def correctHex(possibleHex):
    if (possibleHex.count('h'.upper()) == 1 and possibleHex.endswith('h'.upper())):
        return True
    else:
        return False


def getBytesByString(strOperand):
    pattern = "'(.*?)'"
    substring = re.match(pattern, strOperand).group(1)


def regexMatch(regex, testStr):
    if (re.match('^'+regex+'$', testStr)):
        return True
    else:
        return False

# Analizador Léxico/Sintáctico SIC-XE |
# SIC-XE Lexical and syntax análisis


def passOne(lines):
    calc.onInit()
    global PC
    PC = 0
    initialDirection = 0
    # Por cada linea en el archivo se hace un analisis gramatical |
    # Parse each line in the file
    codOp_LineCounter = 0
    errorDicArray = {}

    for line in lines:  # for each line do
        if (line and line != '\s' and line != '\n' and line != '\t'):
            insertion = "."
            # parse the line and sign values to variables
            label, mnemonic, operands, comment = parseLine(line)
            codop = ""

            if (comment):
                continue
            else:
                dirInstr = SICXE_Dictionary.get(
                    baseMnemonic(mnemonic))  # identify the instruction
                if (operands and (not operands.endswith(",X") or dirInstr[1] == 2)):
                    operandsArray = operands.split(
                        ',')  # split operands with ","
                else:
                    operandsArray = [operands]
                if (not comment):
                    if (dirInstr):  # the instruction exist
                        if (dirInstr[0] == 'I'):  # if is an instruction
                            # if the len of the array returned is 4 means uses operands
                            if (len(dirInstr) == 4):
                                if (operands):  # si hay almenos un operando
                                    # solo se pide un operando
                                    if (len(dirInstr[3]) == 1 and len(operandsArray) == 1):
                                        regAux = argumentTokens[dirInstr[3][0]]
                                        # if(re.match(regAux,operandsArray[0]) or re.match(regAux+',X',operandsArray[0])):
                                        if (regexMatch(regAux+',X', operandsArray[0])):
                                            if ('@' in operandsArray[0]):
                                                insertion = [hex(
                                                    PC), label, mnemonic, operands, "!ERROR!, :Sintaxis:, Direccionamiento indirecto e indexado a la vez ( solo el direccionamieto simple puede ser indexado)"]

                                            elif ('#' in operandsArray[0]):
                                                insertion = [hex(
                                                    PC), label, mnemonic, operands, "!ERROR!, :Sintaxis:, Direccionamiento inmediato e indexado a la vez ( solo el direccionamieto simple puede ser indexado)"]
                                            else:
                                                insertion = [
                                                    hex(PC), label, mnemonic, operands, codop]
                                        elif (regexMatch(regAux, operandsArray[0])):
                                            insertion = [
                                                hex(PC), label, mnemonic, operands, codop]
                                        else:
                                            insertion = [hex(
                                                PC), label, mnemonic, operands, "!ERROR!, :Sintaxis:, El operando no coincide con algun token valido"]

                                    # se piden dos operandos
                                    elif ((len(dirInstr[3]) == 2 and len(operandsArray) == 2)):
                                        regAux = [
                                            argumentTokens[dirInstr[3][0]], argumentTokens[dirInstr[3][1]]]
                                        # if(re.match(regAux[0],operandsArray[0]) and re.match(regAux[1],operandsArray[1])):
                                        if (regexMatch(regAux[0], operandsArray[0]) and regexMatch(regAux[1], operandsArray[1])):
                                            insertion = [
                                                hex(PC), label, mnemonic, operands, codop]
                                        else:  # if any operand is invalid
                                            insertion = [
                                                hex(PC), label, mnemonic, operands, "!ERROR!,:Sintaxis:,uno o mas operandos no validos"]
                                    else:
                                        insertion = [
                                            hex(PC), label, mnemonic, operands, "!ERROR!,:Sintaxis:,Falta  o sobra un operando en la operacion"]
                                else:
                                    insertion = [
                                        hex(PC), label, mnemonic, operands, "!ERROR!,:Sintaxis:,Falta almenos un operando en la operacion"]
                            else:  # means not uses operands
                                if (not operands or operands.startswith('?')):
                                    insertion = [
                                        hex(PC), label, mnemonic, '', '']
                                else:
                                    insertion = [
                                        hex(PC), label, mnemonic, operands, "!ERROR!,:Sintaxis:,sobra un operando"]
                        elif (dirInstr[0] == 'D'):  # is a directive
                            if (dirInstr[1] == 'START'):  # no suma nada
                                if (not label):
                                    insertion = [
                                        hex(PC), label, mnemonic, operands, "!ERROR!,:Sintaxis:,falta nombre de programa"]
                                elif (len(operandsArray) == 1):  # only need one operand
                                    # if(re.match(argumentTokens["dir"],operands)):
                                    if (regexMatch(argumentTokens["dir"], operands)):
                                        insertion = [
                                            hex(PC), label, mnemonic, operands, codop]
                                    else:
                                        insertion = [
                                            hex(PC), label, mnemonic, operands, "!ERROR!,:Sintaxis:,El operando de la directiva no es valido"]
                                else:
                                    insertion = [
                                        hex(PC), label, mnemonic, operands, "!ERROR!,:Sintaxis:,operandos de sobra"]
                                initialDirection = PC
                            elif (dirInstr[1] == 'END'):  # no suma nada
                                if (label):
                                    insertion = [
                                        hex(PC), label, mnemonic, operands, "!ERROR!,:Sintaxis:,la directiva END no lleva label"]
                                # elif(re.match(argumentTokens["[simbol]"],operands)):#only need one operand
                                # only need one operand
                                elif (regexMatch(argumentTokens["[simbol]"], operands)):
                                    insertion = [
                                        hex(PC), label, mnemonic, operands, codop]
                                else:
                                    insertion = [
                                        hex(PC), label, mnemonic, operands, "!ERROR!,:Sintaxis:,El simbolo no es valido"]
                            elif (dirInstr[1] == 'BYTE'):
                                # if(re.match(argumentTokens['[simbol]'],operands) and (re.match(argumentTokens["C'TEXT'"],operands) or re.match(argumentTokens["X'HEX'"],operands)) ):
                                if (regexMatch(argumentTokens['[simbol]'], label) and (regexMatch(argumentTokens["C'TEXT'"], operands) or regexMatch(argumentTokens["X'HEX'"], operands))):
                                    insertion = [
                                        hex(PC), label, mnemonic, operands, codop]
                                else:
                                    insertion = [
                                        hex(PC),  label, mnemonic, operands, "!ERROR!,:Sintaxis:,Operando invalido para BYTE"]
                            elif (dirInstr[1] == 'BASE'):
                                # if(re.match(argumentTokens["[simbol]"],label) and re.match(argumentTokens["simbol"],operands)):
                                if (regexMatch(argumentTokens["[simbol]"], label) and regexMatch(argumentTokens["simbol"], operands)):

                                    insertion = [
                                        hex(PC), label, mnemonic, operands, codop]
                                else:
                                    insertion = [
                                        hex(PC), label, mnemonic, operands, "!ERROR!,Sintaxis:,Operando invalido para BASE"]
                            elif (dirInstr[1] == 'WORD'):
                                # if(re.match(argumentTokens["[simbol]"],label) and re.match(argumentTokens["c"],operands)):
                                if (regexMatch(argumentTokens["[simbol]"], label) and regexMatch(argumentTokens["c"], operands)):

                                    insertion = [
                                        hex(PC), label, mnemonic, operands, codop]
                                else:
                                    insertion = [
                                        hex(PC), label, mnemonic, operands, "!ERROR!,:Sintaxis:,Operando invalido para BASE"]
                            elif (dirInstr[1] == 'RESB'):
                                # if(re.match(argumentTokens["[simbol]"],label) and re.match(argumentTokens["num"],operands)):
                                if (regexMatch(argumentTokens["[simbol]"], label) and regexMatch(argumentTokens["num"], operands)):

                                    insertion = [
                                        hex(PC), label, mnemonic, operands, codop]
                                else:
                                    insertion = [
                                        hex(PC), label, mnemonic, operands, "!ERROR!,:Sintaxis:,Operando invalido para  directiva de reserva"]
                            elif (dirInstr[1] == 'RESW'):
                                # if(re.match(argumentTokens["[simbol]"],label) and re.match(argumentTokens["num"],operands)):
                                if (regexMatch(argumentTokens["[simbol]"], label) and regexMatch(argumentTokens["num"], operands)):

                                    insertion = [
                                        hex(PC), label, mnemonic, operands, codop]
                                else:
                                    insertion = [
                                        hex(PC), label, mnemonic, operands, "!ERROR!,:Sintaxis:,Operando invalido para  directiva de reserva"]
                            elif (dirInstr[1] == 'EQU'):
                                calc.insertSymbol(label, operands)
                            elif (dirInstr[1] == 'USE'):
                                pass
                            elif (dirInstr[1] == 'ORG'):
                                pass
                            elif (dirInstr[1] == 'CSECT'):
                                pass
                            elif (dirInstr[1] == 'EXTDEF'):
                                pass
                            elif (dirInstr[1] == 'EXTREF'):
                                pass
                    else:  # error mnemonico no encontrado.
                        insertion = [
                            hex(PC), label, mnemonic, operands, "!ERROR!,:Mnemonic:,Instruccion no existe"]
                else:
                    codOb.update({codOp_LineCounter: " . "})
                # if there was not a syntax error
                if len(insertion) >= 5:
                    if (not "!ERROR!" in insertion[4]):
                        if (label):
                            if (tabSym.get(label)):  # if the symbol already exist
                                er = [hex(PC), label, mnemonic, operands,
                                      "!ERROR!,:Simbolo:,Simbolo duplicado"]
                                er.insert(0, codOp_LineCounter)
                                errorDicArray.update({codOp_LineCounter: er})
                                insertion.extend(
                                    ["!ERROR!,:Simbolo:,Simbolo duplicado"])
                            elif (mnemonic != "START"):  # else insert the symbol into tabsym
                                tabSym.update({label: hex(PC)})
                            else:  # es el nombre de programa ya que es START
                                nombreDePrograma = label
                        if (dirInstr[0] == 'I'):
                            PC += instruLen(mnemonic)
                        elif (dirInstr[0] == 'D' and dirInstr[1] != 'END'):
                            PC += directiveLen(mnemonic, operands)
                    else:
                        insertionCpy = insertion[:]
                        insertionCpy.insert(0, codOp_LineCounter)
                        errorDicArray.update({codOp_LineCounter: insertionCpy})
                else:
                    {}
                codOb.update({codOp_LineCounter: insertion})
                codOp_LineCounter += 1  # line counter for identify
                if (dirInstr and dirInstr[1] == 'END'):
                    break  # break the loop if the directive END shows up
    tam = PC - initialDirection
    return [codOb, tabSym, initialDirection, tam, errorDicArray]


# Calculo de la direccion objetivo para SIC-XE
# Adressing for SIC-XE
# estas funciones contienen el desplazamiento despejado


Nbit = 32
Ibit = 16
Xbit = 8
Bbit = 4
Pbit = 2
Ebit = 1

# SIMPLE


def flag_Obj_NI(objetiveAddress_TA):
    #TA = desp
    #desp = TA
    res1 = hex(Nbit + Ibit)
    res2 = hex(objetiveAddress_TA)
    return [res1, res2]

# formato 4


def flag_Obj_NIE(objetiveAddress_TA):
    #TA = dir
    #dir = TA
    res1 = hex(Nbit + Ibit + Ebit)
    res2 = hex(objetiveAddress_TA)
    return [res1, res2]


def flag_Obj_NIP(objetiveAddress_TA, CP):
    #TA = (CP) + desp
    #desp = TA - (CP)
    res1 = hex(Nbit + Ibit + Pbit)
    res2 = hex(objetiveAddress_TA - int(CP, 16))
    return [res1, res2]


def flag_Obj_NIB(objetiveAddress_TA, B):
    #TA = (B) + desp
    #desp = TA - (B)
    res1 = hex(Nbit + Ibit + Bbit)
    res2 = hex(objetiveAddress_TA - int(B, 16))
    return [res1, res2]


def flag_Obj_NIX(objetiveAddress_TA):
    # TA = desp + (X) // (X) = 0
    #desp = TA
    res1 = hex(Nbit + Ibit + Xbit)
    res2 = hex(objetiveAddress_TA)
    return [res1, res2]


def flag_Obj_NIXE(objetiveAddress_TA):
    # TA = dir + (X)// (X) = 0
    #desp = TA
    res1 = hex(Nbit + Ibit + Xbit + Ebit)
    res2 = hex(objetiveAddress_TA)
    return [res1, res2]


def flag_Obj_NIXP(objetiveAddress_TA, CP):
    # TA = (CP)+desp+(X)// (X) = 0
    #desp = TA - (CP)
    res1 = hex(Nbit + Ibit + Xbit + Pbit)
    res2 = hex(objetiveAddress_TA - int(CP, 16))
    return [res1, res2]


def flag_Obj_NIXB(objetiveAddress_TA, B):
    # TA = (B)+desp+(X)// (X) = 0
    #desp = TA - (B)
    res1 = hex(Nbit + Ibit + Xbit + Bbit)
    res2 = hex(objetiveAddress_TA - int(B, 16))
    return [res1, res2]

# INDIRECTO


def flag_Obj_N(objetiveAddress_TA):
    #TA = desp
    #desp = TA
    res1 = hex(Nbit)
    res2 = hex(objetiveAddress_TA)
    return [res1, res2]

# formato 4


def flag_Obj_NE(objetiveAddress_TA):
    #TA = dir
    #dir = TA
    res1 = hex(Nbit + Ebit)
    res2 = hex(objetiveAddress_TA)
    return [res1, res2]


def flag_Obj_NP(objetiveAddress_TA, CP):
    #TA = (CP) + desp
    #desp = TA - (CP)
    res1 = hex(Nbit + Pbit)
    res2 = hex(objetiveAddress_TA - int(CP, 16))
    return [res1, res2]


def flag_Obj_NB(objetiveAddress_TA, B):
    #TA = (B) + desp
    #desp = TA -(B)
    res1 = hex(Nbit + Bbit)
    res2 = hex(objetiveAddress_TA - int(B, 16))
    return [res1, res2]

# INMEDIATO


def flag_Obj_I(objetiveAddress_TA):
    #TA = desp
    #desp = TA
    res1 = hex(Ibit)
    res2 = hex(objetiveAddress_TA)
    return [res1, res2]


def flag_Obj_IE(objetiveAddress_TA):
    #TA = dir
    #dir = TA
    res1 = hex(Ibit + Ebit)
    res2 = hex(objetiveAddress_TA)
    return [res1, res2]


def flag_Obj_IP(objetiveAddress_TA, CP):
    #TA = (PC) + desp
    #desp = TA -(PC)
    res1 = hex(Ibit + Pbit)
    res2 = hex(objetiveAddress_TA - int(CP, 16))
    return [res1, res2]


def flag_Obj_IB(objetiveAddress_TA, B):
    #TA = (B) + desp
    #desp = TA - (B)
    res1 = hex(Ibit + Bbit)
    res2 = hex(objetiveAddress_TA - int(B, 16))
    return [res1, res2]

# asumimos que los pasos anteriores se relizaron


def getObjAddr(argument, tab):
    withVariable = False
    argu = baseOperand(argument)
    res = getHexadecimalByString(argu)
    if (res is None):  # it means needs get a value from the symTable
        try:
            res = int(tab.get(argu), 16)
            if (res or res == 0):
                withVariable = True
            else:
                withVariable = ["!ERROR!",
                                "simbolo no encontrado en la tabla de simbolos"]
        except:
            withVariable = ["!ERROR!",
                            "simbolo no encontrado en la tabla de simbolos"]

    return [res, withVariable]


def addressingModes(mnemonic, argument, tab, CP, B):
    OD = getObjAddr(argument, tab)
    auxValueAr = SIC_hex_value(OD[0], True)
    if (isinstance(OD[1], list) and len(OD[1]) > 1):
        return OD[1]
    else:
        if (typeFour(mnemonic)):  # if mnemonic is extended
            # if(re.match('^'+'@'+ argumentTokens.get('m')+'$',argument)):
            if (regexMatch('@' + argumentTokens.get('m'), argument)):
                if (regexMatch('@' + argumentTokens.get('num'), argument)):
                    if not argumentIsA_m_Constant(auxValueAr):
                        return ["!ERROR!", "Modo de direccionamiento no existe, constante fuera de rango"]

                return [flag_Obj_NE(OD[0]), OD[1]]
            # elif(re.match('^'+'#'+ argumentTokens.get('m')+'$',argument)):
            elif (regexMatch('#' + argumentTokens.get('m'), argument)):
                if (regexMatch('#' + argumentTokens.get('num'), argument)):
                    if not argumentIsA_m_Constant(auxValueAr):
                        return ["!ERROR!", "Modo de direccionamiento no existe, constante fuera de rango"]
                # it means is needs to relocate
                return [flag_Obj_IE(OD[0]), OD[1]]
            # elif(re.match('^'+argumentTokens.get('m,X')+'$',argument)):
            elif (regexMatch(argumentTokens.get('m,X'), argument)):
                argu = argument.replace(",X", "")
                if (regexMatch(argumentTokens.get('num'), argu)):
                    if not argumentIsA_m_Constant(auxValueAr):
                        return ["!ERROR!", "Modo de direccionamiento no existe, constante fuera de rango"]

                return [flag_Obj_NIXE(OD[0]), OD[1]]
            # elif(re.match('^'+argumentTokens.get('m')+'$',argument)):
            elif (regexMatch(argumentTokens.get('m'), argument)):
                if (regexMatch(argumentTokens.get('num'), argument)):
                    if not argumentIsA_m_Constant(auxValueAr):
                        return ["!ERROR!", "Modo de direccionamiento no existe, constante fuera de rango"]
                return [flag_Obj_NIE(OD[0]), OD[1]]
            else:
                return ["!ERROR!", "Modo de direccionamiento no existe"]
        else:
            # if(re.match('^'+'#'+ argumentTokens.get('c')+'$',argument)):
            if (regexMatch('#' + argumentTokens.get('c'), argument)):
                if (regexMatch('#' + argumentTokens.get('num'), argument)):
                    if not argumentIsA_c_Constant(auxValueAr):
                        return ["!ERROR!", "Modo de direccionamiento no existe, constante fuera de rango"]
                return [flag_Obj_I(OD[0]), False]
            # elif(re.match('^'+'#'+ argumentTokens.get('m')+'$',argument)):
            elif (regexMatch('#' + argumentTokens.get('m'), argument)):
                if (regexMatch('#' + argumentTokens.get('num'), argument)):
                    if not argumentIsA_m_Constant(auxValueAr):
                        return ["!ERROR!", "Modo de direccionamiento no existe, constante fuera de rango"]
                # can be base or cp relative
                tempIPoIB = [flag_Obj_IP(OD[0], CP), False]
                if (addressIsPCRelative(tempIPoIB[0][1])):
                    return tempIPoIB
                else:
                    tempIPoIB = [flag_Obj_IB(OD[0], B), False]
                    if (addressIsBaseRelative(tempIPoIB[0][1])):
                        return tempIPoIB

                return ["!ERROR!", "Instruccion No es relativa ni a (CP) ni a (B)"]
            # elif(re.match('^'+argumentTokens.get('c,X')+'$',argument)):
            elif (regexMatch(argumentTokens.get('c,X'), argument)):
                argu = argument.replace(",X", "")
                if (regexMatch(argumentTokens.get('num'), argu)):
                    if not argumentIsA_c_Constant(auxValueAr):
                        return ["!ERROR!", "Modo de direccionamiento no existe, constante fuera de rango"]

                return [flag_Obj_NIX(OD[0]), OD[1]]
            # elif(re.match('^'+argumentTokens.get('m,X')+'$',argument)):
            elif (regexMatch(argumentTokens.get('m,X'), argument)):
                # can be base or cp relative
                argu = argument.replace(",X", "")
                if (regexMatch(argumentTokens.get('num'), argu)):
                    if not argumentIsA_m_Constant(auxValueAr):
                        return ["!ERROR!", "Modo de direccionamiento no existe, constante fuera de rango"]

                tempIPoIB = [flag_Obj_NIXP(OD[0], CP), False]
                if (addressIsPCRelative(tempIPoIB[0][1])):
                    return tempIPoIB
                else:
                    tempIPoIB = [flag_Obj_NIXB(OD[0], B), False]
                    if (addressIsBaseRelative(tempIPoIB[0][1])):
                        return tempIPoIB
                return ["!ERROR!", "Instruccion No es relativa ni a (CP) ni a (B)"]
            # elif(re.match('^'+'@'+ argumentTokens.get('c')+'$',argument)):
            elif (regexMatch('@' + argumentTokens.get('c'), argument)):
                if (regexMatch('@' + argumentTokens.get('num'), argument)):
                    if not argumentIsA_c_Constant(auxValueAr):
                        return ["!ERROR!", "Modo de direccionamiento no existe, constante fuera de rango"]

                return [flag_Obj_N(OD[0]), False]
            # elif(re.match('^'+'@'+ argumentTokens.get('m')+'$',argument)):
            elif (regexMatch('@' + argumentTokens.get('m'), argument)):
                if (regexMatch('@' + argumentTokens.get('num'), argument)):
                    if not argumentIsA_m_Constant(auxValueAr):
                        return ["!ERROR!", "Modo de direccionamiento no existe, constante fuera de rango"]

                # can be base or cp relative
                tempIPoIB = [flag_Obj_NP(OD[0], CP), False]
                if (addressIsPCRelative(tempIPoIB[0][1])):
                    return tempIPoIB
                else:
                    tempIPoIB = [flag_Obj_NB(OD[0], B), False]
                    if (addressIsBaseRelative(tempIPoIB[0][1])):
                        return tempIPoIB
                return ["!ERROR!", "Instruccion No es relativa ni a (CP) ni a (B)"]
            # elif(re.match('^'+argumentTokens.get('c')+'$',argument)):
            elif (regexMatch(argumentTokens.get('c'), argument)):
                if (regexMatch(argumentTokens.get('num'), argument)):
                    if not argumentIsA_c_Constant(auxValueAr):
                        return ["!ERROR!", "Modo de direccionamiento no existe, constante fuera de rango"]

                return [flag_Obj_NI(OD[0]), False]
            # elif(re.match('^'+argumentTokens.get('m')+'$',argument)):
            elif (regexMatch(argumentTokens.get('m'), argument)):
                if (regexMatch(argumentTokens.get('num'), argument)):
                    if not argumentIsA_m_Constant(auxValueAr):
                        return ["!ERROR!", "Modo de direccionamiento no existe, constante fuera de rango"]

                # can be base or cp relative
                tempIPoIB = [flag_Obj_NIP(OD[0], CP), False]
                if (addressIsPCRelative(tempIPoIB[0][1])):
                    return tempIPoIB
                else:
                    tempIPoIB = [flag_Obj_NIB(OD[0], B), False]
                    if (addressIsBaseRelative(tempIPoIB[0][1])):
                        return tempIPoIB
                return ["!ERROR!", "Instruccion No es relativa ni a (CP) ni a (B)"]
            else:
                return ["!ERROR!", "Modo de direccionamiento no existe"]
        return ["!ERROR!", "Modo de direccionamiento no existe"]


def byteCodObj(operand):
    strExtract = byteOperandExtract(operand)
    res = ''
    if (operand.startswith('c'.upper())):
        # divided by two becuse each byte uses two nibbles
        strExtract = padHexEven(strExtract).replace("'", "")
        for caracter in strExtract:
            res += format(ord(caracter), 'x')
    elif (operand.startswith('x'.upper())):
        # divided by two becuse each byte uses two nibbles
        res = padHexEven(strExtract).replace("'", "")
    return res

# this function return the binary digit with the specific number of
# bits, if its negative it make the twos complement


def bindigit(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)


def flagsForF3andF4_Decimal(mnemonic, operand):
    resFlags = 0
    if (typeFour(mnemonic)):
        resFlags += Ebit
    if (operand.endswith(",X")):
        resFlags += Xbit
    if (operand[0] == '@'):
        resFlags += Nbit
    elif (operand[0] == '#'):
        resFlags += Ibit
    else:
        resFlags += Nbit+Ibit
    return resFlags


def passTwo(archiInter, symTable):
    codObj = {}  # this function return the codObj
    BASE = 0

    for indexArchi in archiInter:  # forEach line in the intermediateFile
        line = archiInter.get(indexArchi)
        # if there is not error, it means it will make a object code
        if ('ERROR' in line[4] and not 'Simbolo' in line[4]):
            continue  # if there is an error continue without creating ob code
        else:
            infoMnemonic = SICXE_Dictionary.get(baseMnemonic(line[2]))
            #[hex(PC), label, mnemonic, operands, codop]
            # 'BASE'  : ['D','BASE',0],}
            # 'ADD'   : ['I',3,0x18,['m']],
            if (infoMnemonic[1] == 3):
                if (baseMnemonic(line[2]) == 'RSUB'):
                    opAux = int(infoMnemonic[2], 16)
                    op = '{0:08b}'.format(opAux)
                    op = op[:len(op)-2]
                    decFlags = Nbit + Ibit
                    nixbpe = '{0:06b}'.format(decFlags)
                    desp = bindigit(0, 12)
                    finalBinString = op + nixbpe + desp
                    finalHexStr = hex(int(finalBinString, 2))
                    finalHexStr = cleanHexForCodObj(
                        finalHexStr, infoMnemonic[1]*2)
                    # codObj.append(finalHexStr)
                    # codObj[line[0]] = finalHexStr
                    codObj[indexArchi] = finalHexStr
                    archiInter[indexArchi][4] = finalHexStr

                elif (typeFour(line[2])):  # Format 4
                    # op(6)|n|i|x|b|p|e|dir(20)
                    addressingModeRes = addressingModes(
                        line[2], line[3], symTable, archiInter.get(indexArchi+1)[0], BASE)
                    opAux = int(infoMnemonic[2], 16)
                    op = '{0:08b}'.format(opAux)
                    op = op[:len(op)-2]
                    if (addressingModeRes[0] == "!ERROR!"):
                        decFlags = flagsForF3andF4_Decimal(line[2], line[3])
                        decFlags += Bbit + Pbit
                        nixbpe = '{0:06b}'.format(decFlags)
                        dir = bindigit(-1, 20)
                        finalBinString = op + nixbpe + dir
                        finalHexStr = hex(int(finalBinString, 2))
                        finalHexStr = cleanHexForCodObj(
                            finalHexStr, (infoMnemonic[1]+1)*2)
                        finalHexStr += ": " + addressingModeRes[1]
                    else:
                        hexOfFlags = addressingModeRes[0][0]
                        #dir = '{0:020b}'.format(int(addressingModeRes[0][1],16))
                        dir = bindigit(int(addressingModeRes[0][1], 16), 20)
                        #nixbpe = '{0:06b}'.format(int(hexOfFlags,16))
                        nixbpe = bindigit(int(hexOfFlags, 16), 6)
                        finalBinString = op + nixbpe + dir
                        finalHexStr = hex(int(finalBinString, 2))
                        finalHexStr = cleanHexForCodObj(
                            finalHexStr, (infoMnemonic[1]+1)*2)
                        if (addressingModeRes[1] == True):
                            finalHexStr += '*'
                    # codObj.append(finalHexStr)
                    # codObj[line[0]] = finalHexStr
                    codObj[indexArchi] = finalHexStr
                    archiInter[indexArchi][4] = finalHexStr
                else:  # Format 3
                    # op(6)|n|i|x|b|p|e|desp(12)
                    addressingModeRes = addressingModes(
                        line[2], line[3], symTable, archiInter.get(indexArchi+1)[0], BASE)
                    opAux = infoMnemonic[2]
                    op = '{0:08b}'.format(int(opAux, 16))
                    op = op[:len(op)-2]
                    if (addressingModeRes[0] == "!ERROR!"):
                        decFlags = flagsForF3andF4_Decimal(line[2], line[3])
                        decFlags += Bbit + Pbit
                        nixbpe = '{0:06b}'.format(decFlags)
                        dir = bindigit(-1, 12)
                        finalBinString = op + nixbpe + dir
                        finalHexStr = hex(int(finalBinString, 2))
                        finalHexStr = cleanHexForCodObj(
                            finalHexStr, infoMnemonic[1]*2)
                        finalHexStr += ": " + addressingModeRes[1]
                    else:
                        hexOfFlags = addressingModeRes[0][0]
                        #desp = '{0:012b}'.format(int(addressingModeRes[0][1],16))
                        desp = bindigit(int(addressingModeRes[0][1], 16), 12)
                        #nixbpe = '{0:06b}'.format(int(hexOfFlags,16))
                        nixbpe = bindigit(int(hexOfFlags, 16), 6)
                        finalBinString = op + nixbpe + desp
                        finalHexStr = hex(int(finalBinString, 2))
                        finalHexStr = cleanHexForCodObj(
                            finalHexStr, infoMnemonic[1]*2)
                        if (addressingModeRes[1] == True):
                            finalHexStr += '*'
                    # codObj.append(finalHexStr)
                    # codObj[line[0]] = finalHexStr
                    codObj[indexArchi] = finalHexStr
                    archiInter[indexArchi][4] = finalHexStr
            else:
                if (infoMnemonic[1] == 2):  # Format 2
                    # op(8)|r1(4)|r2(4)
                    opAux = int(infoMnemonic[2], 16)
                    op = '{0:08b}'.format(opAux)
                    registersArray = line[3].split(",")

                    r1 = r2On = 0
                    if (infoMnemonic[3] == ['r']):
                        r1 = SIXE_Registers.get(registersArray[0])
                    elif (infoMnemonic[3] == ['n']):
                        r1 = int(registersArray[0])
                    elif (infoMnemonic[3] == ['r', 'r']):
                        r1 = SIXE_Registers.get(registersArray[0])
                        r2On = SIXE_Registers.get(registersArray[1])
                    elif (infoMnemonic[3] == ['r', 'n']):
                        r1 = SIXE_Registers.get(registersArray[0])
                        r2On = int(registersArray[1])-1
                    r1 = bindigit(r1, 4)
                    r2On = bindigit(r2On, 4)
                    finalBinString = op + r1 + r2On
                    finalHexStr = hex(int(finalBinString, 2))
                    finalHexStr = cleanHexForCodObj(
                        finalHexStr, infoMnemonic[1]*2)
                    # codObj.append(finalHexStr)
                    # codObj[line[0]] = finalHexStr
                    codObj[indexArchi] = finalHexStr
                    archiInter[indexArchi][4] = finalHexStr
                elif (infoMnemonic[1] == 1):  # Format 1
                    # op(8)
                    insertionP2 = cleanHexForCodObj(
                        infoMnemonic[2], infoMnemonic[1]*2)
                    # codObj.append(insertionP2)
                    # codObj[line[0]] = insertionP2
                    codObj[indexArchi] = insertionP2
                    archiInter[indexArchi][4] = insertionP2
                elif (infoMnemonic[1] == 'BASE'):
                    rawBASE = getObjAddr(line[3], symTable)[0]
                    BASE = '{0:06X}'.format(rawBASE)
                    codObj[indexArchi] = "----"
                    archiInter[indexArchi][4] = "----"
                elif (infoMnemonic[1] == 'BYTE'):
                    # codObj.append(byteCodObj(line[3]))
                    # codObj[line[0]] = byteCodObj(line[3])
                    codObj[indexArchi] = byteCodObj(line[3])
                    archiInter[indexArchi][4] = byteCodObj(line[3])
                elif (infoMnemonic[1] == 'WORD'):
                    hexAux = SIC_hex_value(line[3], True)
                    bAux = format(int(hexAux, 16), '0>24b')
                    finalHexStr = '{0:06X}'.format(int(bAux, 2))
                    # codObj.append(finalHexStr)
                    # codObj[line[0]] = finalHexStr
                    codObj[indexArchi] = finalHexStr
                    archiInter[indexArchi][4] = finalHexStr
                else:
                    codObj[indexArchi] = "----"
                    archiInter[indexArchi][4] = "----"
    return codObj


def fillOrCutL(strFOC, numFinal=6, charFill='0'):
    if (len(strFOC) < numFinal):
        return strFOC.ljust(numFinal, charFill)
    else:
        return strFOC[0:numFinal]


def fillOrCutR(strFOC, numFinal=6, charFill='0'):
    if (len(strFOC) < numFinal):
        return strFOC.rjust(numFinal, charFill)
    else:
        return strFOC[0:numFinal]


def cleanHexForCodObj(hexa, numFinal=6, charfill='0'):
    if (type(hexa) == str):
        hexAuxi = hexa.replace('0x', '')
        return fillOrCutR(hexAuxi, numFinal, charfill)
    elif (type(hexa) == int):
        return fillOrCutR(int(hexa, 16), numFinal, charfill)


def SIC_hex_value(s, hexi=False):
    try:
        if isinstance(s, int):
            if (hexi):
                exa = hex(s)
                return exa
            return s
        elif (re.match('[0-9a-fA-F]+(H|h)', s)):
            s = s.replace("H", "")
            s = s.replace("h", "")
            if (hexi):
                inte = int(s, 16)
                exa = hex(inte)
                return exa
            return int(s, 16)
        elif (re.match('[0-9]+$', s)):
            if (hexi):
                inte = int(s, 10)
                exa = hex(inte)
                return exa
            return int(s, 10)
    except:
        return hex(0)


def getExpressionValue_(self, input):
    debug = False
    ops_ = ['-', '+', '*', '/']
    operands = []
    one_operand = ''
    operators = []

    # we have a special case; and that is where the input is simply '*'
    if input == '*':
        return t.getCorrespondingNumber('*')

    for bit in input:
        if bit in ops_:
            if len(one_operand) == 0:
                return -1

            # returns [value, 'A' or 'R']
            num = t.getCorrespondingNumber(one_operand)
            if num == -1:
                self.errors.append("Cannot find", one_operand, "in the symtab")
                return -1
            operands.append(num)
            one_operand = ''

            if len(operators) != 0:
                while ops_.index(operators[-1]) >= ops_.index(bit):
                    op1 = operands.pop()  # because we used up 2 operands
                    op2 = operands.pop()
                    abs_or_rel = [op1[1], op2[1]]
                    op1 = op1[0]
                    op2 = op2[0]
                    single = operators.pop()
                    if single == '-':
                        if abs_or_rel != ['R', 'R']:
                            self.errors.append(
                                "Cannot find value of expression; check whether the args are absolute")
                            return
                        operands.append([op2 - op1, 'A'])
                    else:
                        if abs_or_rel != ['A', 'A']:
                            self.errors.append(
                                "Cannot find value of expression; check whether the args are absolute")
                            return
                    if single == '+':
                        operands.append([op2 + op1, 'A'])
                    elif single == '*':
                        operands.append([op2 * op1, 'A'])
                    else:
                        operands.append([op2 // op1, 'A'])
                    if len(operators) == 0:
                        break
            operators.append(bit)
        else:
            one_operand += bit
        if debug:
            print("\n\n")
            print("new bit: ", bit)
            print("operands: ", operands)
            print("operators: ", operators)

    if len(one_operand) == 0:
        return -1
    num = t.getCorrespondingNumber(one_operand)
    if num == -1:
        self.errors.append("Cannot find", one_operand, "in the symtab")
        return
    operands.append(num)

    if debug:
        print("finished main loop")
        print("\n\n")
        print("operands: ", operands)
        print("operators: ", operators)

    while (len(operands) != 1):
        op1 = operands.pop()  # because we used up 2 operands
        op2 = operands.pop()
        abs_or_rel = [op1[1], op2[1]]
        op1 = op1[0]
        op2 = op2[0]
        single = operators.pop()

        if debug:
            print("just before the first iteration")
            print("\n\n")
            print("operands: ", operands)
            print("operators: ", operators)

        if single == '-':
            if abs_or_rel != ['R', 'R']:
                self.errors.append(
                    "Cannot find value of expression; check whether the args are absolute")
                return
            operands.append([op2 - op1, 'A'])
        else:
            if abs_or_rel != ['A', 'A']:
                self.errors.append(
                    "Cannot find value of expression; check whether the args are absolute")
                return
            if single == '+':
                operands.append([op2 + op1, 'A'])
            elif single == '*':
                operands.append([op2 * op1, 'A'])
            else:
                operands.append([op2 // op1, 'A'])
        if debug:
            print("\n\n")
            print("operands: ", operands)
            print("operators: ", operators)

    return operands[0]
