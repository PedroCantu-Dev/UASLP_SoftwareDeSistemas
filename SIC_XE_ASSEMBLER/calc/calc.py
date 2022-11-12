import ply.lex as lex
import ply.yacc as yacc
import sys
import math
import re


######################################################
#
# Definicion de calculadora de expresiones para la SICXE
# con la ayuda de ply: lex y yacc
#
######################################################

# Create a list to hold all of the token names
tokens = [
    'INDEXED',  # --> ,X
    'OCTO',  # -->#
    'AT',  # -->@
    'INTH',
    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
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
    'OR',
    'AND',
    'FACTORIAL',
    'UMINUS'
]

# Use regular expressions to define what each token is
t_OCTO = r'\#'
t_AT = r'\@'
t_LPARENT = r'\('
t_RPARENT = r'\)'
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
t_OR = r'\|\|'
t_AND = r'\&\&'
t_EQUALS = r'\='


# Ply's special t_ignore variable allows us to define characters the lexer will ignore.
# We're ignoring spaces.
t_ignore = ' \t\n'


def t_INDEXED(t):
    r',X'
    t.type = 'INDEXED'
    return t


def t_INTH(t):
    r'[0-9a-fA-F]+(h|H)'  # (\d+(h|H))|
    t.value = getIntByHexOInt(t.value)
    return t


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
    global expError
    global expErrorDescription
    expError = True
    expErrorDescription = "Caracter ilegal:" + \
        t.value + ": en la posision:" + t.lexpos
    # print("Illegal characters:"+t.value+":")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


precedence = (
    ('left', 'NAME'),
    ('left', 'INTH', 'INDEXED'),
    ('left', 'OR', 'AND'),
    ('left', 'MORET', 'LESST', 'MOREEQ', 'LESSEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS', 'FACTORIAL')
)


# can be an expression or an empty
def p_calc(p):
    '''
    calc : expression
        | expression INDEXED
        | empty
    '''
    p[0] = run(p[1].value)

# for validation of expressions with dir mode


def p_calc_octo_at(p):
    '''
    calc : OCTO expression
        | AT expression
    '''
    p[0] = run(p[2].value)


def p_expression_uminus(p):
    '''expression : MINUS expression %prec UMINUS'''
    p[0] = -p[2].value
    # p[0] = ('uminus', p[2])


def p_expression_uni(p):
    '''
    expression : FACTORIAL expression
    '''
    p[0] = (p[1].value, p[2].value)


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
               | expression OR expression
               | expression AND expression

    '''
    p[0] = (p[2].value, p[1].value, p[3].value)


def p_expression_int_float_name(p):
    '''
    expression : INTH
               | INT
               | FLOAT
               | var
    '''
    p[0] = p[1].value


def p_expression_assign(p):
    '''
    expression : NAME EQUALS expression
    '''
    p[0] = ('=', p[1].value, p[3].value)


def p_var_expression(p):
    '''
    var : NAME
    '''
    p[0] = ('var', p[1].value)


def p_expression_parent(p):
    '''
    expression : LPARENT expression RPARENT
    '''
    p[0] = p[2].value


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


def p_error(p):
    global expError
    global expErrorDescription
    if p:
        expErrorDescription = "token: " + p.type + \
            "\ncon valor: " + str(p.value) + \
            "\nen la posisión: " + str(p.lexpos)
        expError = True
        # Just discard the token and tell the parser it's okay.
        # parser.errok()
    else:
        print("Syntax error at EOF")
        expError = True
        expErrorDescription = "tipo: EOF" + "token: " + p.type + \
            "\ncon valor: " + str(p.value) + \
            "\nen la posisión: " + str(p.lexpos)


# variable para definir que
# tipo de operación se está realizando
# i.e.
# "passOneOperation":Para operaciones del paso 1
# "passTwoOperation":Para operaciones del paso 2
# "syntaxOperation":Solo para verificar la sintaxis
operationTypeOption = ''


def run(p):
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            divisor = run(p[2])
            if (divisor > 0):
                return run(p[1]) / run(p[2])
            else:
                return math.inf
        elif p[0] == '%':
            return run(p[1]) % run(p[2])
        elif p[0] == '||':
            if (run(p[1]) > 0 or run(p[2]) > 0):
                return 1
            else:
                return 0
        elif p[0] == '&&':
            if (run(p[1]) > 0 and run(p[2]) > 0):
                return 1
            else:
                return 0
        elif p[0] == '<':
            if (run(p[1]) < run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '>':
            if (run(p[1]) > run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '<=':
            if (run(p[1]) <= run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '>=':
            if (run(p[1]) >= run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '=':
            # codigo original para la calculadora de expresiones completa
            # env[p[1]] = run(p[2])
            # return env[p[1]]
            global expError
            global expErrorDescription
            expError = True
            expErrorDescription = "Caracter invalido '=' dentro de expresion: no se pueden hacer definiciones internas en la expresion"
            return 0
        elif p[0] == 'uminus':
            #print("funciono muminus")
            return -(run(p[1]))
        elif p[0] == 'var':
            global expError
            global expErrorDescription
            try:
                # codigo original:
                # return env[p[1]]
                # para operaciones del paso 1, el mas estricto
                if (operationTypeOption == "passOneOperation"):
                    # hacemos una instancia de la variable de interes:
                    variable = secciones[nameSECT]['tabsym'][p[1]]
                    # si la variable referenciada no es del bloque actual
                    if (variable['block'] != nameBlock):
                        expError = True
                        expErrorDescription = "variable de distinto bloque"
                        return 0
                    else:
                        return variable['dirVal']
                # para operaciones del paso 0 donde
                elif (operationTypeOption == "passTwoOperation"):
                    # hacemos una instancia de la variable de interes:
                    variable = secciones[nameSECT]['tabsym'][p[1]]
                    return variable['dirVal']
                # exclusivamente para analisis sintactico,
                # no nos importa el estado de las variables o la relatividad
                # solo que la expresion sea correcta lexica y sintacticamente
                else:
                    return 0
            except:
                expError = True
                expErrorDescription = "variable inexistente en el ambito"
                return 0
        elif p[0] == '!':
            return math.factorial(int(run(p[1])))
    else:
        # print(p)
        return p

#########################################################################
# Funciones utiles, y a parte necesarias en la calculadora
#########################################################################

# funcion que determina el valor de un numero entero hex o decimal a "decimal integer"
# valida una expresion regular dado un string


def regexMatch(regex, testStr):
    if (re.match('^'+regex+'$', testStr)):
        return True
    else:
        return False


def getIntByHexOInt(strConvert):
    res = None
    if isinstance(strConvert, int):
        res = strConvert
    elif (correctHex(strConvert)):
        strConvert = strConvert.replace('H', '').replace('h', '')
        res = int(strConvert, 16)
    elif (True):
        try:
            res = int(strConvert, 16)
        except:
            res = None
    if (res == None and strConvert.isdecimal()):
        res = int(strConvert)
    return res


def correctHex(possibleHex):
    if (regexMatch('[0-9a-fA-F]+(H|h)', possibleHex)):
        return True
    else:
        return False


def correctBin(possibleBin):
    if (regexMatch('(0|1)+(B|b)', possibleBin)
        or regexMatch('0b(0|1)+', possibleBin)
            or regexMatch('(0|1)+', possibleBin)):
        return True
    else:
        return False


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
        res = cleanHex(hex(getIntByHexOInt(operand)), digits, charfill).upper()
    except:
        res = cleanHex(hex(0), digits, charfill).upper()
    if (hexi):
        res += 'H'
    return res


# def SIC_HEX_ToInt(SIC_HEX):
#     try:
#         if correctHex(SIC_HEX):

###############################################################
#
#       Inician las funciones Utiles de la calculadora
#
###############################################################

#####
#
# Definicion de variables necesarias para el funcionamiento
#
#####
expError = False
expErrorDescription = ""
parser = yacc.yacc()
# arreglo de secciones
secciones = {}
# instancia de seccion
seccion = {}
# instancia de
tabBlock = {}
tabSym = {}

tabBlockRow = {}
tabSymRow = {}

listaCSECTBlockCP = {}

# las variables que tienen que ser inicializadas cada vez que se realize el paso uno -->cambiar por passOneOnInit()


def passOneOnInit():
    global tabBlockRow
    global tabSymRow
    global expError
    global expErrorDescription
    global parser
    global secciones
    global seccion
    global tabBlock
    global tabSym
    tabBlockRow = {}
    tabSymRow = {}
    expError = False
    expErrorDescription = ""
    parser = yacc.yacc()
    # arreglo de secciones
    secciones = {}
    # instancia de seccion
    seccion = {}
    # instancia de
    tabBlock = {}
    tabSym = {}

# las variables que tienen que ser inicializadas cada vez que se realize el paso dos


def passTwoOnInit():
    pass
    # funcion que resuelve las expresiones

# retorna un array con todos los tokens de una expresion dada


def getTokens(expression):
    resTokens = []
    lexer.input(expression)

    while True:
        tok = lexer.token()

        if not tok:
            break
        else:
            # resTokens.append({'type': tok.type, 'value': tok.value})
            resTokens.append(tok)
        print(tok)
    return resTokens


# valida la sintaxis total de la expresion:
# es decir si es correcta lexica y sintacticamente
# sin importarle si los terminos(simbolos) están definidos
errorExSyntax = False
msgExSyntax = ''


def validateExpSyntax(expression):
    global expError
    global expErrorDescription
    global operationTypeOption
    expError = False
    expErrorDescription = ""
    operationTypeOption = "syntaxOperation"
    try:
        parser.parse(expression)
        if (expError == True):
            return expErrorDescription
        else:
            return True
    except:
        return "Error expresion invalida"


# funcion--> evaluateExpSICXE(expression)
# es llamada por las evaluaciones para el paso 1 y el paso 2
# i.e. evaluateExpPassOne() y evaluateExpPassTwo()
def evaluateExpSICXE(expression):
    global expError
    global expErrorDescription
    expError = False
    expErrorDescription = ""
    try:
        value = parser.parse(expression)
        if (expError == True):
            return (False, expErrorDescription)
        else:
            # validacion de relatividad
            relativityValidation = validateExRelativity_A_R_I(expression)
            # si el tamaño de la validacion de relatividad es 1
            # significa que la expresion es correcta por relatividad
            # si no, el error por relatividad estara asignado a la variable
            if (len(relativityValidation) == 1):
                return (True, value, relativityValidation)
            else:
                return (False, relativityValidation)
    except:
        return (False, "Error expresion invalida")


# funcion--> evaluateExpPassOne()
# evalua una expresion para el paso 1
# i.e. todos los simbolos que se utilicen
# deben de estar definidos
# y dentro del el mismo bloque
# NOTA: Si la expresion no es valida bajo
# estos requerimientos retorna False
# dentro de una tupla con la descripcino del error


def evaluateExpPassOne(expression):
    global operationTypeOption
    operationTypeOption = "passOneOperation"
    return evaluateExpSICXE(expression)


# funcion--> evaluateExpPassTwo()
# evalua una expresion para el paso 2
# i.e. todos los simbolos que se utilicen
# deben de estar definidos
# y pueden ser de bloques distintos
# NOTA: Si la expresion no es valida bajo
# estos requerimientos retirna False
# dentro de una tupla con la descripcino del error


def evaluateExpPassTwo(expression):
    global operationTypeOption
    operationTypeOption = "passTwoOperation"
    return evaluateExpSICXE(expression)

# efectua la regla de los signos [(+)*(+) = (+)], [(-)*(-) = (+) ] y [(-)*(+) = (-) ]  para un signo o un array de signos


def singnsRulePositive(signOrSigns):
    if (type(signOrSigns) is list):
        if (len(signOrSigns) == 0):
            return True
        elif (signOrSigns.count('-') % 2 == 0):
            return True
        else:
            return False
    else:
        if (signOrSigns == '+'):
            return True
        else:
            return False

# valida si la expresion es  valida
# y determina si es Absoluta, relativa o invalida por relatividad
# todo mediante el recorrido de la expresion y la ayuda de stacks de operacion


def validateExRelativity_A_R_I(expression):
    tokenes = getTokens(expression)
    Rpos = []
    Rneg = []
    parentesis = []
    operators = []
    RParentPos = []
    RParentNeg = []
    lastToken = ''
    for tok in tokenes:
        if (tok.type == 'MINUS' or tok.type == 'PLUS' or tok.type == 'MULTIPLY' or tok.type == 'DIVIDE'):
            if ((tok.type == 'MULTIPLY' or tok.type == 'DIVIDE') and len(Rpos) != len(Rneg)):
                if (lastToken.type != 'A'):
                    return "ERROR: operador invalido para termino relativo"
            operators.append(tok.value)
        elif (tok.type == 'LPARENT'):
            RParentNeg = []
            LParentPos = []
            if (len(operators) > 0):
                parentesis.append(operators.pop())
            else:
                parentesis.append('+')
        elif (tok.type == 'RPARENT'):
            parOp = parentesis.pop()
            if (parOp == '*' or parOp == '/'):
                if (len(Rpos) != len(Rneg)):
                    return "ERROR: operador invalido para termino relativo"
        elif (tok.type == 'INT' or tok.type == 'INTH'):
            tok.type == 'A'
            if (len(operators) > 0):
                operators.pop()
        elif (tok.type == 'NAME'):
            # comprobar en la tabla si es Relativo o absoluto
            # if (secciones[nameSECT]['tabsym'][tok.value]['typ'] == 'R'):
            # if (input(tok.value+": ") == 'R'):
            if (tok.value == 'R'):
                tok.type == 'R'
                if (singnsRulePositive(parentesis)):
                    if (len(operators) > 0):
                        operator = operators.pop()
                        if (operator == "*" or operator == "/"):
                            return "ERROR: operador invalido para termino relativo"
                        if (singnsRulePositive(operator)):
                            if (len(Rneg) > 0):
                                Rneg.pop()
                            else:
                                Rpos.append(tok.value)
                        else:
                            if (len(Rpos) > 0):
                                Rpos.pop()
                            else:
                                Rneg.append(tok.value)
                    else:
                        if (len(Rneg) > 0):
                            Rneg.pop()
                        else:
                            Rpos.append(tok.value)
                else:
                    if (len(operators) > 0):
                        if (singnsRulePositive(operators.pop())):
                            if (len(Rpos) > 0):
                                Rpos.pop()
                            else:
                                Rneg.append(tok.value)
                        else:
                            if (len(Rneg) > 0):
                                Rneg.pop()
                            else:
                                Rpos.append(tok.value)
                    else:
                        if (len(Rneg) > 0):
                            Rneg.pop()
                        else:
                            Rpos.append(tok.value)
            else:
                tok.type = 'A'
                if (len(operators) > 0):
                    operators.pop()
        lastToken = tok
    if (len(Rpos) == 0 and len(Rneg) == 0):
        # significa que es un termino absoluto
        return 'A'
    elif (len(Rpos) == 1 and len(Rneg) == 0):
        # significa que es un termino relativo
        return 'R'
    else:
        # significa que es un error
        return 'Error: la expresion es invalida por relatividad'


##########################################################
# funciones del Counter Location(Contador de programa: CP)
#########################################################
nameSECT = ''  # nombre de la seccion actual
nameBlock = ''  # nombre del bloque actual
nameSTART = ''  # nombre de la seccion principal y del bloque por omision
locSTART = 0

# cambia el nombre del bloque, se llama con la directiva USE


def setNameBlock(name=''):
    global nameBlock
    if (name):
        nameBlock = name
    else:
        nameBlock = nameSTART

# cambia la seccion de trabajo


def setNameSECT(name=''):
    global nameSECT
    if (name and name in secciones.keys()):
        # error porque se quiere volver a nombrar una seccion de control igual
        return 'Error: Solo se puede definir la seccion de control una vez'
    elif (name):
        nameSECT = name
    else:
        nameSECT = nameSTART
    return True

#####
# Localidades de start
#####


def setLocSTART(location):
    global locSTART
    locSTART = getIntByHexOInt(location)


def gettLocSTART():
    global locSTART
    return locSTART
#####
# Nombres de start( bloque por omision y seccion principal)
#####


def setNameSTART(nameST):
    global nameSTART
    global nameSECT
    global nameBlock
    nameSTART = nameST
    # inicializando los nombres de seccion y bloques por omision
    nameSECT = nameSTART
    nameBlock = nameSTART


def getNameSTART():
    return nameSTART

#############################
# operaciones para las tablas
#############################


def appendSection(name=''):
    global secciones
    name = nameSECT if not name else name

    secciones[name] = {
        'tabblock': {},
        'tabsym': {}}

    appendBlock()


def appendBlock(name='', dirIniRel=0, len=0):
    global secciones
    name = nameBlock if not name else name
    secciones[nameSECT]['tabblock'][name] = {
        'len': len, 'dirIniRel': dirIniRel}


def addSymbol(symbol, dirVal=-1, typ='A', extBool=False, nameBloc=None):
    nameBloc = nameBlock if nameBloc == None else nameBloc
    if (not symbol in secciones[nameSECT]['tabsym'].keys()):
        secciones[nameSECT]['tabsym'][symbol] = {
            'dirVal': SIC_HEX(dirVal), 'type': typ, 'block': nameBloc, 'symExt': extBool
        }
        return True
    else:
        return 'Error: simbolo duplicado'


def updateTabBlockLen(numBlock, len=0, section=nameSECT):
    secciones[section]['tabblock'][numBlock]['len'] = len
# añade una seccion de programa

# suma a CP el numero de bytes indicado


def addToCounterLoc(addition=0):
    secciones[nameSECT]['tabblock'][nameBlock]['len'] += addition


#
def setCounterLoc(counter=0):
    secciones[nameSECT]['tabblock'][nameBlock]['init'] = counter

# retorna el valor del contador de programa de la seccion y bloque actuales


def getCounterLoc():
    return secciones[nameSECT]['tabblock'][nameBlock]['len']

# retorna el valor del contador de programa de la seccion y bloque actuales


def getThisCounterLoc(sectionN=nameSECT, blockN=nameBlock):
    return secciones[sectionN]['tabblock'][blockN]['len']


    #############################
    # zona de pruebas
    #############################
while True:
    try:
        s = input('calc>>')
    except EOFError:
        break
    ss = parser.parse(s)
    sss = s * 2
    print(sss)

    # # Give the lexer some input
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break
    #     print(tok)
    #     try:
    #         s = input('>> ')

    # except EOFError:
    # break
    # parser.parse(s)

    # while True:
    #     sect = input(seccion)
    #     if (sect):
    #         nameSECT = sect

    # para validar las expresiones sintacticamente:
    # lexer = lex.lex()
    # while True:
    #     data = input("expression: ")
    #     # data2 = validateExpSyntax(data)
    #     data2 = regexMatch('[0-9a-fA-F]+(H|h)', data)
    #     if (data2 == True):
    #         print("CORRECT :D\n")
    #     else:
    #         print("D: INCORRECT")
    #         print("expression invalida sintacticamente: " + expErrorDescription+"\n")

    # para obtener los tokens:
    # getTokens(data)

    ################################################
  # lexer.input(data)

    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break
    #     print(tok)
    #################################
    # print(validateExRelativity_A_R_I('4*(SALTO-ETIQ)+TAM+HAFH'))

    # while True:
    #    data = input("expression: ")
    #
    #     print(validateExRelativity_A_R_I(data))

    # retorna un numero como hexadecimal en formato de la arquitectura SICXE
    # print(SIC_HEX(15))
    # print(SIC_HEX('0030'))
    # print(SIC_HEX('0x03'))
    # print(SIC_HEX('5H'))
    # print(SIC_HEX(15, hexi=True))
    # print(SIC_HEX('0030', hexi=True))
    # print(SIC_HEX('0x03', hexi=True))
    # print(SIC_HEX('5H', hexi=True))
