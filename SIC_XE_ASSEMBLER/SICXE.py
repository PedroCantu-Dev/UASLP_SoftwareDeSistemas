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
    'START': ['D', 'START', 0, 'dir'],
    'END': ['D', 'END', 0, '[simbol]'],
    'BYTE': ['D', 'BYTE', -1, 'byteOperands'],
    'WORD': ['D', 'WORD', 3, 'operand'],
    'RESB': ['D', 'RESB', -1, 'num'],
    'RESW': ['D', 'RESW', -1, 'num'],
    'BASE': ['D', 'BASE', 0, 'simbol'],
    # las directivas añadidas para los nuevos features
    'EQU': ['D', 'EQU', 0, 'operand'],
    'USE': ['D', 'USE', 0, '[simbol]'],
    'ORG': ['D', 'ORG', 0, 'operand'],
    # directivas para secciones de control
    'CSECT': ['D', 'CSECT', 0, 'simbol'],
    'EXTDEF': ['D', 'EXTDEF', 0, 'simbolList'],
    'EXTREF': ['D', 'EXTREF', 0, 'simbolList'],
    # todas las instrucciones
    'ADD': ['I', 3, '0x18', 'operand'],
    'ADDF': ['I', 3, '0x58', 'operand'],
    'ADDR': ['I', 2, '0x90', ['r', 'r']],
    'AND': ['I', 3, '0x40', 'operand'],
    'CLEAR': ['I', 2, '0xB4', ['r']],
    'COMP': ['I', 3, '0x28', 'operand'],
    'COMF': ['I', 3, '0x88', 'operand'],
    'COMPR': ['I', 2, '0xA0', ['r', 'r']],
    'DIV': ['I', 3, '0x24', 'operand'],
    'DIVF': ['I', 3, '0x64', 'operand'],
    'DIVR': ['I', 2, '0x9C', ['r', 'r']],
    'FIX': ['I', 1, '0xC4', ''],
    'FLOAT': ['I', 1, '0xC0', ''],
    'HIO': ['I', 1, '0xF4', ''],
    'J': ['I', 3, '0x3C', 'operand'],
    'JEQ': ['I', 3, '0x30', 'operand'],
    'JGT': ['I', 3, '0x34', 'operand'],
    'JLT': ['I', 3, '0x38', 'operand'],
    'JSUB': ['I', 3, '0x48', 'operand'],
    'LDA': ['I', 3, '0x00', 'operand'],
    'LDB': ['I', 3, '0x68', 'operand'],
    'LDCH': ['I', 3, '0x50', 'operand'],
    'LDF': ['I', 3, '0x70', 'operand'],
    'LDL': ['I', 3, '0x08', 'operand'],
    'LDS': ['I', 3, '0x6C', 'operand'],
    'LDT': ['I', 3, '0x74', 'operand'],
    'LDX': ['I', 3, '0x04', 'operand'],
    'LPS': ['I', 3, '0xD0', 'operand'],
    'MUL': ['I', 3, '0x20', 'operand'],
    'MULF': ['I', 3, '0x60', 'operand'],
    'MULR': ['I', 2, '0x98', ['r', 'r']],
    'NORM': ['I', 1, '0xC8', ''],
    'OR': ['I', 3, '0x44', 'operand'],
    'RD': ['I', 3, '0xD8', 'operand'],
    'RMO': ['I', 2, '0xAC', ['r', 'r']],
    'RSUB': ['I', 3, '0x4C', ''],
    'SHIFTL': ['I', 2, '0xA4', ['r', 'n']],
    'SHIFTR': ['I', 2, '0xA8', ['r', 'n']],
    'SIO': ['I', 1, '0xF0', ''],
    'SSK': ['I', 3, '0xEC', 'operand'],
    'STA': ['I', 3, '0x0C', 'operand'],
    'STB': ['I', 3, '0x78', 'operand'],
    'STCH': ['I', 3, '0x54', 'operand'],
    'STF': ['I', 3, '0x80', 'operand'],
    'STI': ['I', 3, '0xD4', 'operand'],
    'STL': ['I', 3, '0x14', 'operand'],
    'STS': ['I', 3, '0x7C', 'operand'],
    'STSW': ['I', 3, '0xE8', 'operand'],
    'STT': ['I', 3, '0x84', 'operand'],
    'STX': ['I', 3, '0x10', 'operand'],
    'SUB': ['I', 3, '0x1C', 'operand'],
    'SUBF': ['I', 3, '0x5C', 'operand'],
    'SUBR': ['I', 2, '0x94', ['r', 'r']],
    'SVC': ['I', 2, '0xB0', ['n']],
    'TD': ['I', 3, '0xE0', 'operand'],
    'TIO': ['I', 1, '0xF8', ''],
    'TIX': ['I', 3, '0x2C', 'operand'],
    'TIXR': ['I', 2, '0xB8', ['r']],
    'WD': ['I', 3, '0xDC', 'operand']}

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

# Valor de las banderas de direccionamiento
# flags value
NIXBPE = ''
Nbit = 32
Ibit = 16
Xbit = 8
Bbit = 4
Pbit = 2
Ebit = 1

# c indica una constante o dir de memoria entre 0 y 4095 --> expresion absoluta
# m indica una direccion de memoria o un valor constante mayor que 4095 -> expresion relativa o absoluta>4095
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
    'operand': "(@|#)?([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9])(,X)?",
    # can be a character constant or a hexadecimal
    'm': "([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9]*)",
    'm,X': "([0-9]+|[0-9a-fA-F]+H|[a-zA-Z]+[a-zA-Z0-9]*),X",
    'n': "[0-9]+$",  # "[0-9]|1[0-6]",
    'r': "(A|X|L|B|S|T|F|PC|SW)",

    # tokens para directivas|
    # addressing tokens
    'simbol': "[a-zA-Z]+[a-zA-Z0-9]*",
    '[simbol]': "([a-zA-Z]+[a-zA-Z0-9]*)*",  # con lo mismo que labels
    'simbolList': "[a-zA-Z]+[a-zA-Z0-9]|[a-zA-Z]+[a-zA-Z0-9](\s?,\s?[a-zA-Z]+[a-zA-Z0-9])*",
    "C'TEXT'": "(C|c)'[a-zA-Z0-9]+'",
    "X'HEX'": "(X|x)'[0-9a-fA-F]+'",
    "byteOperands": "(C|c)\'[a-zA-Z0-9]+\'|(X|x)\'[0-9a-fA-F]+\'",
    "dir": "[0-9]+|[0-9a-fA-F]+H",
    "val": "[0-9]+|[0-9a-fA-F]+H",
    "num": "[0-9]+|[0-9a-fA-F]+H",

    # tokens for operants
    'c': "[0-9]+|[0-9a-fA-F]+H",  # int or a hexadecimal
    'c,X': "([0-9]+|[0-9a-fA-F]+H),X",
}

# dice si una instruccion es tipo 4


def typeFour(mnemonic):
    if mnemonic[0] == "+":
        return True
    return False

# determina si una instruccion es extendida


def isExtended(mnemonic):
    if (mnemonic == baseMnemonic(mnemonic)):
        return False
    else:
        return True

# determina si una instruccion es valida


def validMnemonic(mnemonic):
    if SICXE_Dictionary.get(mnemonic) or (mnemonic.startswith('+') and SICXE_Dictionary.get(baseMnemonic(mnemonic))):
        return True
    else:
        return False


# Regresa el nemonico como tal, sin signo + |
# Return the mnemonic strin with any leading + striped off


def baseMnemonic(mnemonic):
    if mnemonic[0] == "+":
        return mnemonic[1:]
    return mnemonic


# determina si una instruccion pertenece a la arquitectura SIC


def typeSIC(mnemonic):
    if mnemonic in ("FIX" or "FLOAT" or "HIO" or "SIO" or "TIO"):
        return True
    return None

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

# determina si el operando de la directiva byte es una cadena de caracteres


def isCharByte(operands):
    return operands[0] == 'C'


# determina si el operando de la directiva byte representa un numero hexadecimal
def isHexByte(operands):
    return operands[0] == 'X'

# determina si el numero de carateres hexadecimales es par o impar para completar los bytes


def padHexEven(string):
    if (len(string) % 2):
        return '0'+string
    return string


# this function extracts the substring between markers
# extrae los caracteres entre marcadores
def byteOperandExtract(raw_string, start_marker="'", end_marker="'"):
    start = raw_string.index(start_marker) + len(start_marker)
    end = raw_string.index(end_marker, start)
    return raw_string[start:end]

# Retorna 1 si el primer caracter es diferente a espacios lo que quiere decir que hay una etiqueta|
# Return 1 if the first character is different to any type of space, that means it is a label


def haslabel(c):
    return c != ' ' and c != '\t' and c != '\n'

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

# Retorna 1 si la linea omienza con un "?" |
# return 1 if the line begin with point ?


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
    if baseMnemonic(lineWords[0]) in SICXE_Dictionary.keys():
        mnemonic = lineWords[0]
        operands = "".join(lineWords[1:])
    elif baseMnemonic(lineWords[1]) in SICXE_Dictionary.keys():
        label = lineWords[0]
        mnemonic = lineWords[1]
        if (len(lineWords) >= 3):
            operands = "".join(lineWords[2:])
    return (label, mnemonic, operands, '')

# determina el numero de bytes que se tienen que reservar según la instruccion


def instruLen(instru):
    instruDefArray = SICXE_Dictionary.get(baseMnemonic(instru))
    if (instruDefArray[1] == 3):
        if (typeFour(instru)):
            return 4
        else:
            return 3
    elif (instruDefArray[1] == 2):
        return 2
    else:
        return 1

# retorna la cantidad de bytes necesarios segun la directiva |
# return the number of bytes needed deppending of the directive


def directiveLen(directive, operand=''):
    directiveDefArray = SICXE_Dictionary.get(baseMnemonic(directive))
    res = 0
    # BYTE C'Texto' or X'025A'
    if (directiveDefArray[1] == 'BYTE'):  # for byte directive
        strExtract = byteOperandExtract(operand)
        # cada caracter ocupa un byte
        if any(operand.startswith(sub) for sub in ['c', 'C']):
            res = len(strExtract)
        # cada digito hexadecimal ocupa un byte, pero no hay medios bytes por lo que se castea como int
        elif any(operand.startswith(sub) for sub in ['x', 'X']):
            # divided by two becuse each byte uses two nibbles
            res = int(len(padHexEven(strExtract))/2)
    # WORD Valor. El valor puede expresarse en decimal o hexadecimal.
    # genera una constante entera de una palabra(3 bytes)
    elif (directiveDefArray[1] == 'WORD'):
        res = 3
    # RESB Número. el numero puede expresarse en decimal o hexadecimal.
    elif (directiveDefArray[1] == 'RESB'):  # reseva el numero de bytes indicado
        res = calc.getIntBy_SicXe_HexOrInt(operand)
    # RESW Número. Numero puede ser decimal o hexadecimal
    # indica el numero de palabras a reservar
    elif (directiveDefArray[1] == 'RESW'):
        res = 3 * calc.getIntBy_SicXe_HexOrInt(operand)
    return res


def getBytesByString(strOperand):
    pattern = "'(.*?)'"
    substring = re.match(pattern, strOperand).group(1)


# valida los operandos para las instrucciones de formato 2


def validateFormatTwo(instru, operands):
    # Hace un corte de los operandos por el caracter ','
    operandsSplited = operands.split(",")
    instruOperands = instru[3]
    if (len(instruOperands) == 2 and len(operandsSplited) == 2):
        if (calc.regexMatch(argumentTokens[instruOperands[0]], operandsSplited[0]) and calc.regexMatch(argumentTokens[instruOperands[1]], operandsSplited[1])):
            return True
        else:
            return "al menos un operando inválido"
    elif (len(instruOperands) == 1 and len(operandsSplited) == 1):
        if (calc.regexMatch(argumentTokens[instruOperands[0]], operandsSplited[0])):
            return True
        else:
            return "el operando dado no es válido"
    else:
        return "los operandos no coinciden con los requeridos para la instrucción"


# para determinar el valor de las bandera NIXBPE
Nbit = 32
Ibit = 16
Xbit = 8
Bbit = 4
Pbit = 2
Ebit = 1


def flagsValue(mnemonic, operand):
    resFlags = 0
    # tipos de direccionamiento:
    if (operand[0] == '@'):  # Indirecto
        resFlags += Nbit
    elif (operand[0] == '#'):  # inmediato
        resFlags += Ibit
    else:  # simple
        resFlags += Nbit+Ibit
    # si es indexado
    if (operand.endswith(",X")):
        resFlags += Xbit
    # si es extendido:
    if (typeFour(mnemonic)):
        resFlags += Ebit
    return resFlags


################################################
################################################
################################################
################################################
################################################


# Analizador Léxico/Sintáctico SIC-XE |
# SIC-XE Lexical and syntax análisis

def passOne(lines):
    calc.passOneOnInit()
    # Por cada linea en el archivo se hace un analisis gramatical |
    # Parse each line in the file
    errorDicArray = {}
    # banderas para informacion
    firstInstruction = ''
    alredyDirective = False
    alredyEND = False
    errorFlag = False
    errorInsertion = "."
    commentary = ''
    actualCounterLoc = ''
    blockName = ''
    # definicion del archivo intermedio:
    interFile = []
    for line in lines:  # for each line do
        errorFlag = False
        if (line and line != '\s' and line != '\n' and line != '\t'):
            errorInsertion = "."
            commentary = ''
            actualCounterLoc = calc.getCounterLoc()
            blockName = calc.getNameBlock()
            # parse the line and sign values to variables
            label, mnemonic, operands, comment = parseLine(line)
            codop = ""
            if (comment):  # si toda la linea se trata de un comentario continua
                commentary = '?'
                continue
            else:
                # identificando la instruccion en el diccionario
                dirInstr = SICXE_Dictionary.get(
                    baseMnemonic(mnemonic))  # identify the instruction
                if (dirInstr[0] == 'I'):  # si es una instruccion
                    # si aun no hay una primera instruccion definida( util para cuando END no tiene label al final)
                    if (not firstInstruction):
                        firstInstruction = calc.getCounterLoc()
                    if (dirInstr[1] == 3):  # es instruccion formato 3
                        # si la validacion por sintaxis de toda la expresion es correcta.
                        # Esto incluye el modo de direccionamiento y la indexacion
                        # Por lo que mas adelante se asume que todo es correcto en los operandos
                        # si la validacion para los operandos de la instruccion formato 3 es correcta (True)
                        operandValidation = calc.validateExpSyntax(operands)
                        if (operandValidation == True):
                            if (label):
                                successInsertion = calc.addSymbol(
                                    label, 'R', calc.getCounterLoc())
                                # el simbolo ya existe en la tabla de simbolos
                                if (successInsertion != True):
                                    errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                                    ),  label, mnemonic, operands, ":ERROR:Simbolo:"+successInsertion]
                            # suma la cantidad de bytes de la instruccion a el CP
                            calc.addToCounterLoc(instruLen(mnemonic))
                        else:
                            errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                            ),  label, mnemonic, operands, ":ERROR:Sintaxis:Operando invalido,"+operandValidation]
                    # solo las instrucciones formato 3 pueden ser extendidas, por lo que genera un error
                    elif (typeFour(mnemonic)):
                        errorInsertion = [calc.getNameBlock(),
                                          calc.getCounterLoc(
                        ), label, mnemonic, operands,
                            ":ERROR:Mnemonic:la instruccion no puede ser extendida"]
                    else:
                        if (dirInstr[1] == 2):  # es formato 2
                            operandValidation = validateFormatTwo(
                                dirInstr, operands)
                            # si la validacion para los operandos de la instruccion formato 2 es correcta (True)
                            if (operandValidation == True):
                                # suma 2 bytes al contador de programa actual
                                if (label):
                                    # suma 2 bytes al contador de programa actual
                                    successInsertion = calc.addSymbol(
                                        label, 'R', calc.getCounterLoc())
                                    if (successInsertion != True):
                                        errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                                        ),  label, mnemonic, operands, ":ERROR:Simbolo:successInsertion"]
                                # suma la cantidad de bytes de la instruccion a el CP
                                calc.addToCounterLoc(instruLen(mnemonic))
                            else:
                                errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                                ), label, mnemonic, operands, ":ERROR:Sintaxis:Operando invalido, "+operandValidation]
                        elif (dirInstr[1] == 1):  # es formato 1
                            # si hay operandos para instrucciones formato 1, ocurre un error
                            if (operands):
                                errorInsertion = [calc.getNameBlock(),
                                                  calc.getCounterLoc(
                                ), label, mnemonic, operands, ":ERROR:Sintaxis:sobran operandos"]
                            else:
                                # suma la cantidad de bytes de la instruccion a el CP
                                calc.addToCounterLoc(instruLen(mnemonic))
                        else:
                            errorInsertion = [calc.getNameBlock(),
                                              calc.getCounterLoc(
                            ), label, mnemonic, operands, ":ERROR:Unknowed:unreachable"]
                      # si no hubo error de sintaxis
                elif (dirInstr[0] == 'D'):  # es una directiva
                    if (dirInstr[1] == 'START'):  # no suma nada
                        # si el nombre de programa ya ha sido definido
                        if (calc.getNameSTART() != ''):
                            errorInsertion = [calc.getNameBlock(),
                                              calc.getCounterLoc(
                            ),  label, mnemonic, operands, ":ERROR:Sintaxis:Uso incorrecto de la directiva START, debe ir solo al inicio del programa"]
                        else:
                            if (not label):
                                errorInsertion = [calc.getNameBlock(),
                                                  calc.getCounterLoc(
                                ),  label, mnemonic, operands, "!ERROR!,:Sintaxis:,falta nombre de programa"]
                            elif (calc.regexMatch(argumentTokens[dirInstr[3]], operands)):
                                # define el nombre del programa
                                calc.setNameSTART(label)
                                # define la locacion inicial del programa
                                calc.setLocSTART(operands)
                                # añade una nueva seccion, la seccion inicial
                                calc.appendSection(appendBlock=False)
                                calc.appendBlock(dirIniRel=operands)

                                blockName = calc.getNameBlock()
                                actualCounterLoc = calc.getCounterLoc()
                            else:
                                errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                                ), label, mnemonic, operands, ":ERROR:Sintaxis:operando invalido para la directiva START"]
                    # cambia la seccion de control que se está utilizando
                    elif (dirInstr[1] == 'CSECT'):
                        alredyDirective = False
                        if (label):
                            if (not operands):
                                if (calc.regexMatch(argumentTokens[dirInstr[3]], label)):
                                    successInsertion = calc.appendSection(
                                        label)
                                    if (successInsertion != True):
                                        errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                                        ), label, mnemonic, operands, ":ERROR:Sección:" + successInsertion]
                                    else:
                                        actualCounterLoc = calc.getCounterLoc()
                                        blockName = calc.getNameBlock()
                                else:
                                    errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                                    ), label, mnemonic, operands, ":ERROR:Sintaxis:Nombre invalido para CSECT, se espera un sibolo"]
                            else:
                                errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                                ), label, mnemonic, operands, ":ERROR:Sintaxis:La directiva CSECT no soporta operandos"]
                        else:
                            errorInsertion = [calc.getCounterLoc(
                            ), label, mnemonic, operands, ":ERROR:Sintaxis:Falta el nombre de la seccion de control"]
                    elif (dirInstr[1] == 'EXTDEF'):
                        if (calc.regexMatch(argumentTokens[dirInstr[3]], operands) != True):
                            errorInsertion = [calc.getCounterLoc(
                            ), label, mnemonic, operands, ":ERROR:Sintaxis:Operando invalido para la directiva EXTDEF"]
                    elif (dirInstr[1] == 'EXTREF'):
                        if (calc.regexMatch(argumentTokens[dirInstr[3]], operands) == True):
                            calc.addEXTREF(operands)
                        else:
                            errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                            ), label, mnemonic, operands, ":ERROR:Sintaxis:Operando invalido para la directiva EXTDEF"]
                     # cambia el bloque en el que se está trabajando
                    elif (dirInstr[1] == 'USE'):
                        if (label):
                            errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                            ), label, mnemonic, operands, ":ERROR:Sintaxis:la directiva USE no soporta etiquetas"]
                        else:
                            alredyDirective = True
                            calc.setNameBlock(operands)
                            actualCounterLoc = calc.getCounterLoc()
                            blockName = calc.getNameBlock()
                    # genera una entrada en la tabla de simbolos, segun el bloque y la seccion de control que se esté utilizando
                    elif (dirInstr[1] == 'EQU'):
                        alredyDirective = True
                        if (label):
                            successInsertion = ''
                            # retorna una tupla con información
                            if (operands == '*'):
                                CLoc = calc.getCounterLoc()
                                successInsertion = calc.addSymbol(
                                    label, 'R', CLoc)
                                if (successInsertion != True):
                                    errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                                    ),  label, mnemonic, operands, "ERROR:Simbolo:"+successInsertion]
                            else:
                                operandValidation = calc.evaluateExpPassOne(
                                    operands)
                                if (operandValidation[0] == False):
                                    successInsertion = calc.addSymbol(
                                        label, 'A', -1)
                                    if (successInsertion != True):
                                        errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                                        ), label, mnemonic, operands, ":ERROR:Sintaxis:"+operandValidation[1]+"ERROR:Simbolo:"+successInsertion]
                                    else:
                                        errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                                        ),  label, mnemonic, operands, ":ERROR:Sintaxis:"+operandValidation[1]]
                                else:
                                    successInsertion = calc.addSymbol(
                                        label, operandValidation[1], operandValidation[2])
                                    if (successInsertion != True):
                                        errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                                        ),  label, mnemonic, operands, "ERROR:Simbolo:"+successInsertion]
                        else:
                            errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                            ),  label, mnemonic, operands, ":ERROR:Sintaxis:Definicion de simbolo invalida, falta nombre de simbolo"]
                    # cambia el contador de programa el valor especificado
                    elif (dirInstr[1] == 'ORG'):
                        alredyDirective = True
                        # retorna una tupla con información
                        operandValidation = calc.evaluateExpPassOne(operands)
                        if (operandValidation[0] == False):
                            errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                            ), label, mnemonic, operands, "ERROR:Sintaxis:"+operandValidation[1]]
                        elif (operandValidation[1] == 'R'):
                            errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                            ), label, mnemonic, operands, ":ERROR:Operando:"+"el operando no puede ser relativo"]
                        else:
                            calc.setCounterLoc(operandValidation[2])
                    elif (dirInstr[1] == 'BYTE'):
                        alredyDirective = True
                        if (calc.regexMatch(argumentTokens[dirInstr[3]], operands)):
                            # el simbolo ya existe en la tabla de simbolos
                            if (label):
                                successInsertion = calc.addSymbol(
                                    label, 'R', calc.getCounterLoc())
                                # el simbolo ya existe en la tabla de simbolos
                                if (successInsertion != True):
                                    errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(), calc.getNameBlock(
                                    ), label, mnemonic, operands, ":ERROR:Simbolo:"+successInsertion]
                            calc.addToCounterLoc(
                                directiveLen('BYTE', operands))
                        else:
                            errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                            ), label, mnemonic, operands, "!ERROR!,:Sintaxis:,Operando invalido para BYTE"]
                    # cambia el valor de la base, empieza en -1 comp2
                    elif (dirInstr[1] == 'BASE'):
                        alredyDirective = True
                    elif (dirInstr[1] == 'WORD'):  # suma 3 bytes
                        alredyDirective = True
                        operandValidation = calc.validateExpSyntax(operands)
                        if (operandValidation == True):
                            if (label):
                                successInsertion = calc.addSymbol(
                                    label, 'R', calc.getCounterLoc())
                                # el simbolo ya existe en la tabla de simbolos
                                if (successInsertion != True):
                                    errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(), calc.getNameBlock(
                                    ), label, mnemonic, operands, ":ERROR:Simbolo:"+successInsertion]
                            calc.addToCounterLoc(directiveLen('WORD'))
                        else:
                            errorInsertion = [calc.getNameBlock(),
                                              calc.getCounterLoc(
                            ), label, mnemonic, operands, ":ERROR:Sintaxis:Operando invalido:"+operandValidation]
                    elif (dirInstr[1] == 'RESB'):  # reserva el numero de bytes especificado
                        alredyDirective = True
                        if (calc.regexMatch(argumentTokens[dirInstr[3]], operands)):
                            if (label):
                                successInsertion = calc.addSymbol(
                                    label, 'R', calc.getCounterLoc())
                                # el simbolo ya existe en la tabla de simbolos
                                if (successInsertion != True):
                                    errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                                    ), label, mnemonic, operands, ":ERROR:Simbolo:"+successInsertion]
                            calc.addToCounterLoc(
                                directiveLen('RESB', operands))
                        else:
                            errorInsertion = [
                                calc.getCounterLoc(
                                ), calc.getNameBlock(), label, mnemonic, operands, ":ERROR:Sintaxis:Operando invalido para a directiva RESB"]
                    elif (dirInstr[1] == 'RESW'):
                        alredyDirective = True
                        if (calc.regexMatch(argumentTokens[dirInstr[3]], operands)):
                            if (label):
                                successInsertion = calc.addSymbol(
                                    label, 'R', calc.getCounterLoc())
                                # el simbolo ya existe en la tabla de simbolos
                                if (successInsertion != True):
                                    errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                                    ), label, mnemonic, operands, ":ERROR:Simbolo:"+successInsertion]
                            calc.addToCounterLoc(
                                directiveLen('RESW', operands))
                        else:
                            errorInsertion = [
                                calc.getCounterLoc(
                                ), calc.getNameBlock(), label, mnemonic, operands, ":ERROR:Sintaxis:Operando invalido para a directiva RESW"]
                    elif (dirInstr[1] == 'END'):  # no suma nada
                        if (alredyEND == True):
                            errorInsertion = [calc.getNameBlock(), calc.getCounterLoc(
                            ), label, mnemonic, operands, "!ERROR!,:Sintaxis:,la directiva END debe ir solo al final del programa"]
                        else:
                            alredyEND = True
                            calc.setEND()
                            actualCounterLoc = calc.getCounterLoc()
                            blockName = calc.getNameBlock()
                    # quiere decir que no hubo errores de sintaxis
        if (errorInsertion != "."):
            interFile.append(errorInsertion)
        elif (commentary != "?" and line != ''):
            interFile.append(
                [blockName, actualCounterLoc, label, mnemonic, operands, '.'])
        else:
            interFile.append('.')
    # actualiza todas las tablas de bloques para que queden en la direccion inicial que les corresponde
    calc.updateTabBlocks()
    resPassOne = calc.secciones
    return resPassOne

    # tam = PC - initialDirection
    # return [codOb, tabSym, initialDirection, tam, errorDicArray]

# Calculo de la direccion objetivo para SIC-XE
# Adressing for SIC-XE
# estas funciones contienen el desplazamiento despejado


# asumimos que los pasos anteriores se relizaron


def getObjAddr(argument, tab):
    withVariable = False
    argu = baseOperand(argument)
    res  # = getHexadecimalByString(argu)
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
            # [hex(PC), label, mnemonic, operands, codop]
            # 'BASE'  : ['D','BASE',0],}
            # 'ADD'   : ['I',3,0x18,['m']],
            if (infoMnemonic[1] == 3):
                if (baseMnemonic(line[2]) == 'RSUB'):
                    opAux = int(infoMnemonic[2], 16)
                    n = 9
                    op = '{0:0b}'.format(opAux)
                    op = op[: len(op)-2]
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
                        # dir = '{0:020b}'.format(int(addressingModeRes[0][1],16))
                        dir = bindigit(int(addressingModeRes[0][1], 16), 20)
                        # nixbpe = '{0:06b}'.format(int(hexOfFlags,16))
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
                        # desp = '{0:012b}'.format(int(addressingModeRes[0][1],16))
                        desp = bindigit(int(addressingModeRes[0][1], 16), 12)
                        # nixbpe = '{0:06b}'.format(int(hexOfFlags,16))
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
