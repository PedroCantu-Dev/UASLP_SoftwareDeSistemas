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
    if (mnemonic):
        if mnemonic[0] == "+":
            return mnemonic[1:]
    return mnemonic


# determina si una instruccion pertenece a la arquitectura SIC


def typeSIC(mnemonic):
    if mnemonic in ("FIX" or "FLOAT" or "HIO" or "SIO" or "TIO"):
        return True
    return None

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
    sectName = ''

    # definicion del archivo intermedio:
    interFile = []
    errorsFile = []
    lineIndex = 0
    for line in lines:  # for each line do
        errorFlag = False
        if (line and line != '\s' and line != '\n' and line != '\t'):
            errorInsertion = "."
            commentary = ''
            actualCounterLoc = calc.getCounterLoc()
            blockName = calc.getNameBlock()
            sectName = calc.getNameSECT()
            # parse the line and sign values to variables
            label, mnemonic, operands, comment = parseLine(line)
            codop = ""
            if (comment):  # si toda la linea se trata de un comentario continua
                commentary = '?'
                continue
            else:
                # identificando la instruccion en el diccionario
                # print(line)
                dirInstr = SICXE_Dictionary.get(
                    baseMnemonic(mnemonic))  # identify the instruction
                if (not dirInstr):
                    lineSplited = line.split()
                    label = ""
                    for lineS in lineSplited:
                        label += lineS+" "
                    mnemonic = ''
                    operands = ''
                    errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                    ),  label, mnemonic, operands, ":ERROR:Mnemonic:"+"instruccion no existe"]
                elif (dirInstr[0] == 'I'):  # si es una instruccion
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
                                    errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                                    ),  label, mnemonic, operands, ":ERROR:Simbolo:"+successInsertion]
                            # suma la cantidad de bytes de la instruccion a el CP
                            calc.addToCounterLoc(instruLen(mnemonic))
                        else:
                            errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                            ),  label, mnemonic, operands, ":ERROR:Sintaxis:Operando invalido,"+operandValidation]
                    # solo las instrucciones formato 3 pueden ser extendidas, por lo que genera un error
                    elif (typeFour(mnemonic)):
                        errorInsertion = [lineIndex, sectName, blockName,
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
                                        errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                                        ),  label, mnemonic, operands, ":ERROR:Simbolo:successInsertion"]
                                # suma la cantidad de bytes de la instruccion a el CP
                                calc.addToCounterLoc(instruLen(mnemonic))
                            else:
                                errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                                ), label, mnemonic, operands, ":ERROR:Sintaxis:Operando invalido, "+operandValidation]
                        elif (dirInstr[1] == 1):  # es formato 1
                            # si hay operandos para instrucciones formato 1, ocurre un error
                            if (operands):
                                errorInsertion = [lineIndex, sectName, blockName,
                                                  calc.getCounterLoc(
                                                  ), label, mnemonic, operands, ":ERROR:Sintaxis:sobran operandos"]
                            else:
                                # suma la cantidad de bytes de la instruccion a el CP
                                calc.addToCounterLoc(instruLen(mnemonic))
                        else:
                            errorInsertion = [lineIndex, sectName, blockName,
                                              calc.getCounterLoc(
                                              ), label, mnemonic, operands, ":ERROR:Unknowed:unreachable"]
                      # si no hubo error de sintaxis
                elif (dirInstr[0] == 'D'):  # es una directiva
                    if (dirInstr[1] == 'START'):  # no suma nada
                        # si el nombre de programa ya ha sido definido
                        if (calc.getNameSTART() != ''):
                            errorInsertion = [lineIndex, sectName, blockName,
                                              calc.getCounterLoc(
                                              ),  label, mnemonic, operands, ":ERROR:Sintaxis:Uso incorrecto de la directiva START, debe ir solo al inicio del programa"]
                        else:
                            if (not label):
                                errorInsertion = [lineIndex, sectName, blockName,
                                                  calc.getCounterLoc(
                                                  ),  label, mnemonic, operands, ":ERROR:Sintaxis:Falta nombre de programa"]
                            elif (calc.regexMatch(argumentTokens[dirInstr[3]], operands)):
                                # define el nombre del programa
                                calc.setNameSTART(label)
                                # define la locacion inicial del programa
                                calc.setLocSTART(operands)
                                # añade una nueva seccion, la seccion inicial
                                calc.appendSection(appendBlock=False)
                                calc.appendBlock(dirIniRel=operands)

                                blockName = calc.getNameBlock()
                                sectName = calc.getNameSECT()
                                actualCounterLoc = calc.getCounterLoc()
                            else:
                                errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
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
                                        errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                                        ), label, mnemonic, operands, ":ERROR:Sección:" + successInsertion]
                                    else:
                                        actualCounterLoc = calc.getCounterLoc()
                                        blockName = calc.getNameBlock()
                                        sectName = calc.getNameSECT()
                                else:
                                    errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                                    ), label, mnemonic, operands, ":ERROR:Sintaxis:Nombre invalido para CSECT, se espera un sibolo"]
                            else:
                                errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                                ), label, mnemonic, operands, ":ERROR:Sintaxis:La directiva CSECT no soporta operandos"]
                        else:
                            errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                            ), label, mnemonic, operands, ":ERROR:Sintaxis:Falta el nombre de la seccion de control"]
                    elif (dirInstr[1] == 'EXTDEF'):
                        if (calc.regexMatch(argumentTokens[dirInstr[3]], operands) != True):
                            errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                            ), label, mnemonic, operands, ":ERROR:Sintaxis:Operando invalido para la directiva EXTDEF"]
                    elif (dirInstr[1] == 'EXTREF'):
                        if (calc.regexMatch(argumentTokens[dirInstr[3]], operands) == True):
                            calc.addEXTREF(operands)
                        else:
                            errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                            ), label, mnemonic, operands, ":ERROR:Sintaxis:Operando invalido para la directiva EXTDEF"]
                     # cambia el bloque en el que se está trabajando
                    elif (dirInstr[1] == 'USE'):
                        if (label):
                            errorInsertion = [lineIndex, sectName, blockName,  calc.getCounterLoc(
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
                                    errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                                    ),  label, mnemonic, operands, "ERROR:Simbolo:"+successInsertion]
                            else:
                                operandValidation = calc.evaluateExpPassOne(
                                    operands)
                                if (operandValidation[0] == False):
                                    successInsertion = calc.addSymbol(
                                        label, 'A', -1)
                                    if (successInsertion != True):
                                        errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                                        ), label, mnemonic, operands, ":ERROR:Sintaxis:"+operandValidation[1]+"ERROR:Simbolo:"+successInsertion]
                                    else:
                                        errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                                        ),  label, mnemonic, operands, ":ERROR:Sintaxis:"+operandValidation[1]]
                                else:
                                    successInsertion = calc.addSymbol(
                                        label, operandValidation[1], operandValidation[2])
                                    if (successInsertion != True):
                                        errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                                        ),  label, mnemonic, operands, "ERROR:Simbolo:"+successInsertion]
                        else:
                            errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                            ),  label, mnemonic, operands, ":ERROR:Sintaxis:Definicion de simbolo invalida, falta nombre de simbolo"]
                    # cambia el contador de programa el valor especificado
                    elif (dirInstr[1] == 'ORG'):
                        alredyDirective = True
                        # retorna una tupla con información
                        operandValidation = calc.evaluateExpPassOne(operands)
                        if (operandValidation[0] == False):
                            errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                            ), label, mnemonic, operands, "ERROR:Sintaxis:"+operandValidation[1]]
                        elif (operandValidation[1] == 'R'):
                            errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
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
                                    errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(), calc.getNameBlock(
                                    ), label, mnemonic, operands, ":ERROR:Simbolo:"+successInsertion]
                            calc.addToCounterLoc(
                                directiveLen('BYTE', operands))
                        else:
                            errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                            ), label, mnemonic, operands, ":ERROR:Sintaxis:Operando invalido para BYTE"]
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
                                    errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(), calc.getNameBlock(
                                    ), label, mnemonic, operands, ":ERROR:Simbolo:"+successInsertion]
                            calc.addToCounterLoc(directiveLen('WORD'))
                        else:
                            errorInsertion = [lineIndex, sectName, blockName,
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
                                    errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                                    ), label, mnemonic, operands, ":ERROR:Simbolo:"+successInsertion]
                            calc.addToCounterLoc(
                                directiveLen('RESB', operands))
                        else:
                            errorInsertion = [lineIndex,
                                              sectName, blockName, calc.getCounterLoc(), label, mnemonic, operands, ":ERROR:Sintaxis:Operando invalido para a directiva RESB"]
                    elif (dirInstr[1] == 'RESW'):
                        alredyDirective = True
                        if (calc.regexMatch(argumentTokens[dirInstr[3]], operands)):
                            if (label):
                                successInsertion = calc.addSymbol(
                                    label, 'R', calc.getCounterLoc())
                                # el simbolo ya existe en la tabla de simbolos
                                if (successInsertion != True):
                                    errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                                    ), label, mnemonic, operands, ":ERROR:Simbolo:"+successInsertion]
                            calc.addToCounterLoc(
                                directiveLen('RESW', operands))
                        else:
                            errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                            ), label, mnemonic, operands, ":ERROR:Sintaxis:Operando invalido para a directiva RESW"]
                    elif (dirInstr[1] == 'END'):  # no suma nada
                        if (alredyEND == True):
                            errorInsertion = [lineIndex, sectName, blockName, calc.getCounterLoc(
                            ), label, mnemonic, operands, ":ERROR:Sintaxis:la directiva END debe ir solo al final del programa"]
                        else:
                            alredyEND = True
                            calc.setEND()
                            actualCounterLoc = calc.getCounterLoc()
                            blockName = calc.getNameBlock()
                            sectName = calc.getNameSECT()
                    # quiere decir que no hubo errores de sintaxis
        if (errorInsertion != "."):
            interFile.append(errorInsertion)
            errorsFile.append(errorInsertion)
        elif (commentary != "?" and line != ''):
            interFile.append(
                [lineIndex, sectName, blockName, actualCounterLoc, label, mnemonic, operands, '.'])
        else:
            interFile.append('.')
        lineIndex += 1
    # actualiza todas las tablas de bloques para que queden en la direccion inicial que les corresponde
    calc.updateTabBlocks()
    return {'nameSTART': calc.getNameSTART(), 'secciones': calc.secciones, 'interFile': interFile, 'errorsFile': errorsFile}

    # tam = PC - initialDirection
    # return [codOb, tabSym, initialDirection, tam, errorDicArray]

# Calculo de la direccion objetivo para SIC-XE
# Adressing for SIC-XE
# estas funciones contienen el desplazamiento despejado


# asumimos que los pasos anteriores se relizaron
# determina si una direccion es relativa a la base, esta tiene que ser hexadecimal |
# determine if a given address is relative to the base, the address must be in hexadecimal


def addressIsBaseRelative(address):
    if address >= 0 and address <= 4096:
        return True
    else:
        return False

# determina si una direccion es relativa al contador de programa, esta tiene que ser hexadecimal |
# determine if a given address is relative to program counter, the address must be in hexadecimal


def addressIsPCRelative(address):
    if address >= -2048 and address <= 2047:
        return True
    else:
        return False

# determina si el operando de la directiva byte es una cadena de caracteres


def isCharByte(operands):
    return operands[0] == 'C'


# determina si el operando de la directiva byte representa un numero hexadecimal
def isHexByte(operands):
    return operands[0] == 'X'

# return True if the range of the costant is between 0 and 4095


def argumentIsA_c_Constant(argument):
    if (argument >= 0 and argument <= 4095):
        return True
    else:
        return False

# return True if the range of the costant is between grader than 4095


def argumentIsA_m_Constant(argument):
    if (argument > 4095):
        return True
    else:
        return False


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

# devuelve las el valor de las banderas y el valor de la expresion


def addressingModes(mnemonic, operands, line, nextLine):
    nixbpe = flagsValue(mnemonic, operands)
    passTwoExpValidation = calc.evaluateExpPassTwo(operands)
    externalFlag = False
    if passTwoExpValidation[0] == False:
        # return (True, relativityValidation, value)
        # return (False, relativityValidation)
        # return (False, "Error expresion invalida")
        # error en expresion paso 2
        nixbpe += Pbit + Bbit
        res = {'valid': False, 'nixbpe': nixbpe,
               'msg': passTwoExpValidation[1], 'passTwoExpValidation': passTwoExpValidation}
    else:
        target = passTwoExpValidation[2]
        typeExpression = passTwoExpValidation[1]
        # if ('@' in operands or '#' in operands):  # direccionamiento Indirecto
        if typeExpression == 'E':
            # pasTwoValidation returns: (True, 'E', value, extTermsInOperation, relativityValidation)
            # relativityValidations returns(when applyRules flag in False): {'relativePositive': Rpos, 'relativeNegative': Rneg}
            return {'valid': typeExpression, 'nixbpe': nixbpe, 'dirOrDesp': target, 'passTwoExpValidation': passTwoExpValidation}
        elif typeFour(mnemonic):  # si es extendido: TA = dir
            res = {'valid': typeExpression, 'nixbpe': nixbpe, 'dirOrDesp': target,
                   'passTwoExpValidation': passTwoExpValidation}
        elif typeExpression == 'A':  # si es una constante c: TA = desp
            if (argumentIsA_c_Constant(target)):
                res = {'valid': typeExpression, 'nixbpe': nixbpe, 'dirOrDesp': target,
                       'passTwoExpValidation': passTwoExpValidation}
            elif (argumentIsA_m_Constant(target)):
                targetRes = target - \
                    (calc.getIntBy_SicXe_HexOrInt(
                        line[3]) + 3)  # pasar el valor de cp de la siguiente linea
                # relaitvo a CP
                # si es una constante m: TA = CP +desp
                if addressIsPCRelative(targetRes):
                    nixbpe += Pbit
                    res = {'valid': typeExpression, 'nixbpe': nixbpe, 'dirOrDesp': targetRes,
                           'passTwoExpValidation': passTwoExpValidation}
                else:
                    # pasar nombre de seccion
                    targetRes = target - calc.getBASE(line[1])
                    # relativo a la Base
                    # si es una constante m: TA = B +desp
                    if addressIsBaseRelative(targetRes):
                        nixbpe += Bbit
                        res = {'valid': typeExpression, 'nixbpe': nixbpe, 'dirOrDesp': targetRes,
                               'passTwoExpValidation': passTwoExpValidation}
                    else:  # ERROR , no relativo a base ni a cp
                        nixbpe += Bbit + Pbit
                        res = {'valid': False, 'nixbpe': nixbpe, 'msg': "No relativo ni a CP ni a base",
                               'passTwoExpValidation': passTwoExpValidation}
            else:  # ERROR:operando fuera de rango
                res = {'valid': False, 'nixbpe': nixbpe, 'msg': "Operando fuera de rango",
                       'passTwoExpValidation': passTwoExpValidation}
        elif typeExpression == 'R':  # se toma como m
            # pasar el valor de cp de la siguiente linea
            targetRes = target - (calc.getIntBy_SicXe_HexOrInt(line[3]) + 3)
            if addressIsPCRelative(targetRes):  # relativo a CP
                nixbpe += Pbit
                res = {'valid': typeExpression, 'nixbpe': nixbpe, 'dirOrDesp': targetRes,
                       'passTwoExpValidation': passTwoExpValidation}
            else:
                targetRes = target - calc.getBASE(line[1])
                if addressIsBaseRelative(targetRes):  # relativo a Base
                    nixbpe += Bbit
                    res = {'valid': typeExpression, 'nixbpe': nixbpe, 'dirOrDesp': targetRes,
                           'passTwoExpValidation': passTwoExpValidation}
                else:  # error , no relativo a base ni a cp
                    nixbpe += Bbit + Pbit
                    res = {'valid': False, 'nixbpe': nixbpe,
                           'msg': "No relativo ni a CP ni a Base"}
    return res


def passTwo(archiInter, secciones):
    codObj = {}  # this function return the codObj
    codesObj = {}
    registersDefAndRef = []
    registersT = []
    registersM = []
    regDef = ['D']
    regRef = ['R']
    regT = ['T']
    regM = ['M']
    regE = ['E']

    BASE = 0
    # for line in archiInter:  # forEach line in the intermediateFile
    for line in enumerate(archiInter):  # forEach line in the intermediateFile
        # if there is not error, it means it will make a object code
        line = line[1]

        numOfBytes = 0
        # sino existe error se genera cdigo objeto .
        if (line != '.' and line[7] == '.' and line[5] != 'EQU'):
            mnemonic = line[5]
            baseMnem = baseMnemonic(mnemonic)
            infoMnemonic = SICXE_Dictionary.get(baseMnem)
            if (infoMnemonic):
                if (infoMnemonic[0] == 'I'):
                    opAux = int(infoMnemonic[2], 16)
                    op = calc.bindigit(opAux, 8)
                    op = op[: len(op)-2]
                    if (infoMnemonic[1] == 3):
                        numOfBytes = 3
                        if (baseMnem == 'RSUB'):
                            decFlags = Nbit + Ibit
                            nixbpe = '{0:06b}'.format(decFlags)
                            desp = calc.bindigit(0, 12)
                            finalBinString = op + nixbpe + desp
                        else:
                            addrMode = addressingModes(
                                mnemonic, line[6], line, archiInter[line[0]+1])
                            if (addrMode['valid'] == False):
                                # append error msg
                                nixbpe = '{0:06b}'.format(addrMode['nixbpe'])
                                if (typeFour(mnemonic)):
                                    dirOrDesp = calc.bindigit(-1, 20)
                                else:
                                    dirOrDesp = calc.bindigit(-1, 12)
                                finalBinString = op + nixbpe + dirOrDesp
                            elif (typeFour(mnemonic)):  # Format 4
                                numOfBytes = 4
                                # op(6)|n|i|x|b|p|e|dir(20)
                                nixbpe = '{0:06b}'.format(addrMode['nixbpe'])
                                dir = calc.bindigit(addrMode['dirOrDesp'], 20)
                                finalBinString = op + nixbpe + dir
                            else:  # Formato 3
                                # op(6)|n|i|x|b|p|e|desp(12)
                                nixbpe = '{0:06b}'.format(addrMode['nixbpe'])
                                desp = calc.bindigit(addrMode['dirOrDesp'], 12)
                                finalBinString = op + nixbpe + desp
                        finalHexStr = hex(int(finalBinString, 2))
                        finalHexStr = calc.SIC_HEX(
                            finalHexStr, numOfBytes*2)

                        # pasTwoValidation returns: (True, 'E', value, extTermsInOperation, relativityValidation)
                        # relativityValidations returns(when applyRules flag in False): {'relativePositive': Rpos, 'relativeNegative': Rneg}
                        finalHexStrForCodobj = finalHexStr
                        if (addrMode['valid'] == 'E'):
                            passTwoExpValidation = addrMode['passTwoExpValidation']
                            for externComplete in passTwoExpValidation[3]:
                                extern = externComplete.split('|')[2]
                                finalHexStr += '*SE'
                                finalHexStrForCodobj += "*SE|"+externComplete
                            if (len(passTwoExpValidation[4]['relativePositive']) > len(passTwoExpValidation[4]['relativeNegative'])):
                                for relPosTerm in passTwoExpValidation[4]['relativePositive']:
                                    finalHexStr += '*R'
                                    finalHexStrForCodobj += "*R|"+relPosTerm
                            elif (len(passTwoExpValidation[4]['relativeNegative']) > len(passTwoExpValidation[4]['relativePositive'])):
                                for relNegTerm in passTwoExpValidation[4]['relativeNegative']:
                                    finalHexStr += '*R'
                                    finalHexStrForCodobj += "*R|"+relNegTerm

                        elif (addrMode['valid'] == 'R'):
                            if (typeFour(mnemonic)):
                                finalHexStr += '*R'
                                finalHexStrForCodobj = finalHexStr
                        codObj[line[0]] = finalHexStrForCodobj
                        line[7] = finalHexStr

                        tToAppend = finalHexStr.split('*')[0]
                        if len(regT[-1]) <= 1:
                            regT[-1] += line[3]+"??"
                            regT[-1] += tToAppend
                        elif (len(regT[-1]) + len(tToAppend) > 70):
                            subRegT = regT[-1][regT[-1].index('??')+2:]
                            lengthCodObj = int(len(subRegT)/2)
                            lengthCodObj = calc.SIC_HEX(lengthCodObj, 2)
                            regT[-1] = regT[-1].replace('??', lengthCodObj)
                            regT.append['T']
                            regT[-1] += line[3]
                            regT[-1] += tToAppend
                        else:
                            regT[-1] += tToAppend
                    elif (infoMnemonic[1] == 2):  # formato 2
                        # op(8)|r1(4)|r2(4)
                        opAux = int(infoMnemonic[2], 16)
                        op = '{0:08b}'.format(opAux)
                        registersArray = line[6].split(",")

                        r1 = r2On = 0
                        if (infoMnemonic[3] == ['r']):
                            r1 = SIXE_Registers[registersArray[0]]
                        elif (infoMnemonic[3] == ['n']):
                            # es esto correcto ??
                            r1 = int(registersArray[0])-1
                        elif (infoMnemonic[3] == ['r', 'r']):
                            r1 = SIXE_Registers[registersArray[0]]
                            r2On = SIXE_Registers[registersArray[1]]
                        elif (infoMnemonic[3] == ['r', 'n']):
                            r1 = SIXE_Registers[registersArray[0]]
                            r2On = int(registersArray[1])-1
                        r1 = calc.bindigit(r1, 4)
                        r2On = calc.bindigit(r2On, 4)
                        finalBinString = op + r1 + r2On
                        finalHexStr = hex(int(finalBinString, 2))
                        finalHexStr = calc.SIC_HEX(
                            finalHexStr, infoMnemonic[1]*2)
                        # codObj.append(finalHexStr)
                        # codObj[line[0]] = finalHexStr
                        codObj[line[0]] = finalHexStr
                        line[7] = finalHexStr
                        tToAppend = finalHexStr.split('*')[0]
                        if len(regT[-1]) <= 1:
                            regT[-1] += line[3]+"??"
                            regT[-1] += tToAppend
                        elif (len(regT[-1]) + len(tToAppend) > 70):
                            subRegT = regT[-1][regT[-1].index('??')+2:]
                            lengthCodObj = int(len(subRegT)/2)
                            lengthCodObj = calc.SIC_HEX(lengthCodObj, 2)
                            regT[-1] = regT[-1].replace('??', lengthCodObj)
                            regT.append['T']
                            regT[-1] += line[3]
                            regT[-1] += tToAppend
                        else:
                            regT[-1] += tToAppend
                    elif (infoMnemonic[1] == 1):  # formato 1
                        # op(8)
                        insertionP2 = calc.SIC_HEX(
                            infoMnemonic[2], infoMnemonic[1]*2)
                        # codObj.append(insertionP2)
                        # codObj[line[0]] = insertionP2
                        codObj[line[0]] = insertionP2
                        line[7] = insertionP2
                        tToAppend = finalHexStr.split('*')[0]
                        if len(regT[-1]) <= 1:
                            regT[-1] += line[3]+"??"
                            regT[-1] += tToAppend
                        elif (len(regT[-1]) + len(tToAppend) > 70):
                            subRegT = regT[-1][regT[-1].index('??')+2:]
                            lengthCodObj = int(len(subRegT)/2)
                            lengthCodObj = calc.SIC_HEX(lengthCodObj, 2)
                            regT[-1] = regT[-1].replace('??', lengthCodObj)
                            regT.append['T']
                            regT[-1] += line[3]
                            regT[-1] += tToAppend
                        else:
                            regT[-1] += tToAppend
                elif (baseMnem == 'WORD'):
                    passTwoExpValidation = calc.evaluateExpPassTwo(line[6])
                    if (passTwoExpValidation[0] == True):
                        target = passTwoExpValidation[2]
                        finalBinString = calc.bindigit(
                            target, 24)
                    else:
                        finalBinString = calc.bindigit(
                            -1, 24)
                    finalHexStr = hex(int(finalBinString, 2))
                    finalHexStr = calc.SIC_HEX(
                        finalHexStr, 3*2)
                    # pasTwoValidation returns: (True, 'E', value, extTermsInOperation, relativityValidation)
                    # relativityValidations returns(when applyRules flag in False): {'relativePositive': Rpos, 'relativeNegative': Rneg}
                    finalHexStrForCodobj = finalHexStr
                    if (passTwoExpValidation[1] == 'R'):
                        finalHexStr += '*R'
                        finalHexStrForCodobj = finalHexStr
                    elif (passTwoExpValidation[1] == 'E'):
                        for externComplete in passTwoExpValidation[3]:
                            extern = externComplete.split('|')[2]
                            finalHexStr += '*SE'
                            finalHexStrForCodobj += "*SE|"+externComplete
                        if (len(passTwoExpValidation[4]['relativePositive']) > len(passTwoExpValidation[4]['relativeNegative'])):
                            for relPosTerm in passTwoExpValidation[4]['relativePositive']:
                                finalHexStr += '*R'
                                finalHexStrForCodobj += "*R|"+relPosTerm
                        elif (len(passTwoExpValidation[4]['relativeNegative']) > len(passTwoExpValidation[4]['relativePositive'])):
                            for relNegTerm in passTwoExpValidation[4]['relativeNegative']:
                                finalHexStr += '*R'
                                finalHexStrForCodobj += "*R|"+relNegTerm
                    codObj[line[0]] = finalHexStrForCodobj
                    line[7] = finalHexStr
                    tToAppend = finalHexStr.split('*')[0]
                    if len(regT[-1]) <= 1:
                        regT[-1] += line[3]+"??"
                        regT[-1] += tToAppend
                    elif (len(regT[-1]) + len(tToAppend) > 70):
                        subRegT = regT[-1][regT[-1].index('??')+2:]
                        lengthCodObj = int(len(subRegT)/2)
                        lengthCodObj = calc.SIC_HEX(lengthCodObj, 2)
                        regT[-1] = regT[-1].replace('??', lengthCodObj)
                        regT.append['T']
                        regT[-1] += line[3]
                        regT[-1] += tToAppend
                    else:
                        regT[-1] += tToAppend

                elif (baseMnem == 'BYTE'):
                    codObject = byteCodObj(line[6])
                    codObj[line[0]] = codObject
                    line[7] = codObject
                    tToAppend = codObject.split('*')[0]
                    if len(regT[-1]) <= 1:
                        regT[-1] += line[3]+"??"
                        regT[-1] += tToAppend
                    elif (len(regT[-1]) + len(tToAppend) > 70):
                        subRegT = regT[-1][regT[-1].index('??')+2:]
                        lengthCodObj = int(len(subRegT)/2)
                        lengthCodObj = calc.SIC_HEX(lengthCodObj, 2)
                        regT[-1] = regT[-1].replace('??', lengthCodObj)
                        regT.append['T']
                        regT[-1] += line[3]
                        regT[-1] += tToAppend
                    else:
                        regT[-1] += tToAppend
                elif (baseMnem == 'BASE'):
                    pass
                elif (baseMnem == 'CSECT'):
                    if len(regDef[-1]) <= 1:
                        regDef.pop()
                    if len(regRef[-1]) <= 1:
                        regRef.pop()
                    if len(regT[-1]) <= 1:
                        regT.pop()
                        subRegT = regT[-1][regT[-1].index('??')+2:]
                        lengthCodObj = int(len(subRegT)/2)
                        lengthCodObj = calc.SIC_HEX(lengthCodObj, 2)
                        regT[-1] = regT[-1].replace('??', lengthCodObj)
                    else:
                        subRegT = regT[-1][regT[-1].index('??')+2:]
                        lengthCodObj = int(len(subRegT)/2)
                        lengthCodObj = calc.SIC_HEX(lengthCodObj, 2)
                        regT[-1] = regT[-1].replace('??', lengthCodObj)
                    if len(regM[-1]) <= 1:
                        regM.pop()
                    if len(regE[-1]) <= 1:
                        regE.pop()
                    regFilePseudoFinal = calc.concatenateListContent(
                        registersDefAndRef, '\n')+calc.concatenateListContent(regT, '\n')+calc.concatenateListContent(regM, '\n')
                    codesObj[calc.getNameSECT()] = {regFilePseudoFinal}
                    calc.setNameSECTPassTwo(line[1])
                    calc.setNameBlockPassTwo(line[2])
                    regDef = ['D']
                    regRef = ['R']
                    regT = ['T']
                    regM = ['M']
                    regE = ['E']
                    registersDefAndRef = []
                elif (baseMnem == 'EXTDEF'):
                    for extDef in line[6].split(','):
                        if len(regDef[-1])+12 > 73:
                            registersDefAndRef.append(regDef[-1])
                            regDef.append('D')
                        else:
                            nomBlock = secciones[calc.getNameSECT(
                            )]['tabsym'][extDef]['block']
                            dirVal = calc.getIntBy_SicXe_HexOrInt(
                                secciones[calc.getNameSECT()]['tabsym'][extDef]['dirVal'], True)
                            dirBlock = calc.getIntBy_SicXe_HexOrInt(
                                secciones[calc.getNameSECT()]['tabblock'][nomBlock]['dirIniRel'], True)
                            regDef[-1] += calc.fillOrCutL(
                                extDef, 6, ' ') + calc.SIC_HEX(dirVal + dirBlock)
                    registersDefAndRef.append(regDef[-1])
                    regDef.append('D')
                elif baseMnem == 'EXTREF':
                    for extRef in line[6].split(','):
                        if len(regRef[-1])+6 > 73:
                            registersDefAndRef.append(regRef[-1])
                            regRef.append('R')
                        else:
                            regRef[-1] += calc.fillOrCutL(extRef, 6, ' ')
                    registersDefAndRef.append(regRef[-1])
                    regRef.append('R')
                elif (baseMnem == 'RESW' or baseMnem == 'RESB' or baseMnem == 'ORG' or baseMnem == 'USE'):
                    if (len(regT[-1]) > 1):
                        subRegT = regT[-1][regT[-1].index('??')+2:]
                        lengthCodObj = int(len(subRegT)/2)
                        lengthCodObj = calc.SIC_HEX(lengthCodObj, 2)
                        regT[-1] = regT[-1].replace('??', lengthCodObj)
                        regT.append('T')
                    if (baseMnem == 'USE'):
                        calc.setNameBlockPassTwo(line[2])
                if (baseMnem == 'END'):
                    if len(regDef[-1]) <= 1:
                        regDef.pop()
                    if len(regRef[-1]) <= 1:
                        regRef.pop()
                    if len(regT[-1]) <= 1:
                        regT.pop()
                        subRegT = regT[-1][regT[-1].index('??')+2:]
                        lengthCodObj = int(len(subRegT)/2)
                        lengthCodObj = calc.SIC_HEX(lengthCodObj, 2)
                        regT[-1] = regT[-1].replace('??', lengthCodObj)
                    else:
                        subRegT = regT[-1][regT[-1].index('??')+2:]
                        lengthCodObj = int(len(subRegT)/2)
                        lengthCodObj = calc.SIC_HEX(lengthCodObj, 2)
                        regT[-1] = regT[-1].replace('??', lengthCodObj)
                    if len(regM[-1]) <= 1:
                        regM.pop()
                    if len(regE[-1]) <= 1:
                        regE.pop()
                    regFilePseudoFinal = calc.concatenateListContent(
                        registersDefAndRef, '\n')+calc.concatenateListContent(regT, '\n')+calc.concatenateListContent(regM, '\n')
                    codesObj[calc.getNameSECT()] = {regFilePseudoFinal}

    return {'codObj': codObj}
