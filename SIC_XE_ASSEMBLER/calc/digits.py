import re

#######################################################################
# funciones para manejar muneros dentro de la arquitectura SicXe
#######################################################################


def regexMatch(regex, testStr):
    if (re.match('^'+regex+'$', testStr)):
        return True
    else:
        return False


def bindigit(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)


def twosComplement(binaryNumber):
    onesComplement = ''
    for binDigit in binaryNumber:
        if binDigit == '0':
            onesComplement += '1'
        elif binDigit == '1':
            onesComplement += '0'
    res = int(onesComplement, 2) + 1
    res = bindigit(res, len(binaryNumber))
    return res


def correctSicXeHex(possibleHex):
    if (regexMatch('[0-9a-fA-F]+(H|h)', possibleHex)):
        return True
    else:
        return False


def getIntBy_SicXe_HexOrInt(strConvert, dir=False):
    res = 0
    if isinstance(strConvert, int):
        res = strConvert
    elif (correctSicXeHex(strConvert)):
        strConvert = strConvert.replace('H', '').replace('h', '')
        res = bindigit(int(strConvert, 16), len(strConvert)*4)
        if (len(res) > 0 and res[0] == '1'):  # es un numero negativo
            res = - int(twosComplement(res), 2)
        else:
            res = int(strConvert, 16)
    elif (strConvert.isdecimal() and dir == False):
        res = int(strConvert)
    else:
        try:
            res = int(strConvert, 16)
        except:
            res = 0
    return res

#############################################################################
# Obtener un numero hexadecimal con representacion de la arquitectura SICXE
#############################################################################


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


def cleanHex(hexa, numFinal=6, charfill='0'):
    if (type(hexa) == str):
        hexAuxi = hexa.replace('0x', '')
        return fillOrCutR(hexAuxi, numFinal, charfill)
    elif (type(hexa) == int):
        return fillOrCutR(int(hexa, 16), numFinal, charfill)

# retorna un numero como hexadecimal en formato de la arquitectura SICXE


def SIC_HEX(operand=0, digits=6, charfill='0', hexi=False):
    try:
        if (isinstance(operand, int) and operand < 0):
            res = bindigit(operand, digits*4)
            res = cleanHex(hex(int(res, 2)), digits)
        else:
            res = cleanHex(hex(getIntBy_SicXe_HexOrInt(operand)),
                           digits, charfill)
    except:
        res = cleanHex(hex(0), digits, charfill)
    if (hexi):
        res += 'H'
    return str(res).upper()


#####################################
# Zona de pruebas
#####################################


print(SIC_HEX(15, 3))
print(SIC_HEX(15, 6))
print(SIC_HEX(15))
print(SIC_HEX(15, 7))
print(SIC_HEX(-1))
print(SIC_HEX(-1, 12))
print(SIC_HEX(-3))
print(SIC_HEX(-3, 12))
print("los get int")
print(getIntBy_SicXe_HexOrInt('0010', True))
print(getIntBy_SicXe_HexOrInt('0010', False))
print(getIntBy_SicXe_HexOrInt('0010'))
###############################
# print(SIC_HEX(15, hexi=True))
# print(SIC_HEX('0030', hexi=True))
# print(SIC_HEX('0x03', hexi=True))
# print(SIC_HEX('5H', hexi=True))
