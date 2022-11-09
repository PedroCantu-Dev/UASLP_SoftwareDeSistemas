import ply.lex as lex
import ply.yacc as yacc
import sys
import math

# Create a list to hold all of the token names
tokens = [
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


# More complicated tokens, such as tokens that are more than 1 character in length
# are defined using functions.
# A float is 1 or more numbers followed by a dot (.) followed by 1 or more numbers again.


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INTH(t):
    r'\d+H|(A|B|C|D|E|F)+\d*H^'
    t.value = getIntByHexOInt(t.value)
    return t

# An int is 1 or more numbers.


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


# at this point the lexical analyzer made its work so, it suóse there is not error whenhex parsing


def getIntByHexOInt(strConvert):
    res = None
    if (strConvert.isdecimal()):
        res = int(strConvert)
    elif (correctHex(strConvert)):
        if ("h" in strConvert):
            res = int(strConvert.replace("h", ""), 16)
        else:
            res = int(strConvert.replace("h".upper(), ""), 16)
    return res


def correctHex(possibleHex):
    if (('h' in possibleHex or 'H' in possibleHex) and (possibleHex.endswith('h'.upper()) or possibleHex.endswith('h'))):
        return True
    else:
        return False

# A NAME is a variable name. A variable can be 1 or more characters in length.
# The first character must be in the ranges a-z A-Z or be an underscore.
# Any character following the first character can be a-z A-Z 0-9 or an underscore.


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'NAME'
    return t


# Skip the current token and output 'Illegal characters' using the special Ply t_error function.


def t_error(t):
    global err
    global errorDescription
    errorDescription = "Illegal characters:"+t.value+":"
    print("Illegal characters:"+t.value+":")
    t.lexer.skip(1)
    err = True


# Build the lexer

lexer = lex.lex()


precedence = (
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
         | empty
    '''
    print(run(p[1].value))


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


def p_expression_int_float_name(p):
    '''
    expression : INT
               | FLOAT
               | var
    '''
    p[0] = p[1].value


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
    global err
    global errorDescription
    if p:
        print("syntax error en el token: " + p.type +
              "\ncon valor: " + str(p.value) + "\nen la linea: " + str(p.lineno))

        errorDescription = "syntax error en el token: " + p.type + \
            "\ncon valor: " + str(p.value) + "\nen la linea: " + str(p.lineno)
        err = True
        # Just discard the token and tell the parser it's okay.
        # parser.errok()
    else:
        print("Syntax error at EOF")
        err = True
        errorDescription = "Syntax error en EOF"


# while True:
#     try:
#         s = input('calc>>')
#     except EOFError:
#         break
#     print(parser.parse(s))

#####
#
# Variables necesarias para el funcionamiento
#
#####

err = False
errorDescription = ""
varUSE = "omision"
varSECT = "omision"
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


def onInit():
    global tabBlockRow
    global tabSymRow
    global err
    global errorDescription
    global varUSE
    global varSECT
    global parser
    global secciones
    global seccion
    global tabBlock
    global tabSym
    tabBlockRow = {}
    tabSymRow = {}
    err = False
    errorDescription = ""
    varUSE = "omision"
    varSECT = "omision"
    parser = yacc.yacc()
    # arreglo de secciones
    secciones = {}
    # instancia de seccion
    seccion = {}
    # instancia de
    tabBlock = {}
    tabSym = {}


def run(p):
    global err
    global errorDescription
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
            try:
                # env[p[1]] = run(p[2])
                # return env[p[1]]
                appendTabSymRow(p[1], run(p[2]),
                                validateExRelativity_A_R_I(p[2]), False)
                return secciones[varSECT]['tabsym'][p[1]]['dirVal']

            except:
                errorDescription = "variable inexistente en el ambito 2"
                err = True
                return 0
        elif p[0] == 'uminus':
            print("funciono muminus")
            return -(run(p[1]))
        elif p[0] == 'var':
            try:
                # return env[p[1]]
                return secciones[varSECT]['tabsym'][p[1]]['dirVal']
            except:
                errorDescription = "variable inexistente en el ambito 1"
                err = True
                return 0

        elif p[0] == '!':
            return math.factorial(int(run(p[1])))
    else:
        # print(p)
        return p


# while True:
#     try:
#         errorDescription = ""
#         err = False
#         s = input('calc>> ')
#     except EOFError:
#         err = True
#         errorDescription = "EOF"
#         break
#     parser.parse(s)
#     if (err == True):
#         print(":::ERROR::: " + errorDescription)
#     else:
#         print("well done")


# Ensure our parser understands the correct order of operations.
# The precedence variable is a special Ply variable.
# precedence = (

#     ('left', 'PLUS', 'MINUS'),
#     ('left', 'MULTIPLY', 'DIVIDE')

# )

# Test it out
# data = '''
#  3 + 4 * 10
#    + -20 / 34 >=2 >(ssdR- 50) || 45<(89)*!76 <= 45
#  '''

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

def changeUSE(name=''):
    global varUSE
    if (name):
        varUSE = name
    else:
        varUSE = "omision"


arrayBlocks = []


def changeSECT(name=''):
    global varSECT
    if (name and name in secciones.keys()):
        pass  # error porque se quiere volver a nombrar una seccion de control igual
    elif (name):
        varSECT = name
    else:
        varSECT = "omision"


def listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1


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


# valida la sintaxys total de la expresion:
# es decir si es correcta lexica y sintacticamente
# sin importarle si los terminos(simbolos) están definidos


def validateExSyntax(expression):
    global err
    err = False
    global errorDescription
    errorDescription = ""
    try:
        parser.parse(expression)
        if (err == True):
            if ("inexistente" in errorDescription):
                return True
            else:
                return (False, errorDescription)
        else:
            return True
    except:
        return (False, "Error expresion invalida")

# valida la sintaxys total de la expresion:
# es decir si es correcta lexica y sintacticamente
# sin importarle si los terminos(simbolos) están definidos


def validateExSyntaxAndVariables(expression):
    global err
    err = False
    global errorDescription
    errorDescription = ""
    try:
        parser.parse(expression)
        if (err == True):
            return (False, errorDescription)
        else:
            return True
    except:
        return (False, ":::Error expresion invalida :::")

# valida si la expresion es  valida
# y determina si es Absoluta, relativa o invalida por relatividad


def signsRulePoitive(signOrSigns):
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


def validateExRelativity_A_R_I(expression):
    tokenes = getTokens(expression)
    Rpos = []
    Rneg = []
    parentesis = []
    operators = []
    for tok in tokenes:
        if (tok.type == 'MINUS' or tok.type == 'PLUS' or tok.type == 'MULTIPLY' or tok.type == 'DIVIDE'):
            operators.append(tok.value)
        elif (tok.type == 'LPARENT'):
            if (len(operators) > 0):
                parentesis.append(operators.pop())
            else:
                parentesis.append('+')
        elif (tok.type == 'RPARENT'):
            parentesis.pop()
        elif (tok.type == 'INT'):
            if (len(operators) > 0):
                operators.pop()
        elif (tok.type == 'NAME'):
            # comprobar en la tabla si es Relativo o absoluto
            # if (secciones[varSECT]['tabsym'][tok.value]['typ'] == 'R'):
            if (input(tok.value+": ") == 's'):
                if (signsRulePoitive(parentesis)):
                    if (len(operators) > 0):
                        operator = operators.pop()
                        if (operator == "*" or operator == "/"):
                            return "ERROR: operador invalido para termino relativo"
                        if (signsRulePoitive(operator)):
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
                        if (signsRulePoitive(operators.pop())):
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
                if (len(operators) > 0):
                    operators.pop()
    if (len(Rpos) == 0 and len(Rneg) == 0):
        # significa que es un termino absoluto
        return 'A'
    elif (len(Rpos) == 1 and len(Rneg) == 0):
        # significa que es un termino relativo
        return 'R'
    else:
        # significa que es un error
        return 'Error: la expresion es invalida por relatividad'

# determina si las operaciones de expresiones son válidas,
# es decir que no se utilicen terminos relativos
# para operaciones como multiplicación o división


def validateExRelativityOp(expression):
    pass


#############################
# operaciones para las tablas
#############################
blockCounter = 0


def appendTabSymRow(symbol, dirVal, typ, extBool, numBlock):
    if (not symbol in secciones[varSECT]['tabsym'].keys()):
        secciones[varSECT]['tabsym'].append({symbol: {
            'dirVal': dirVal, 'typ': typ, 'numBlock': numBlock, 'extBool': extBool}})
    else:
        pass  # error simbolo duplicado


def appendTabBlockRow(numBlock, name, len=0, dirIniRel=0):
    secciones[varSECT]['tabblock'].append({numBlock: {
        'name': name, 'len': len, 'dirIniRel': dirIniRel}})


def updateTabBlockLen(numBlock, len=0, section=varSECT):
    secciones[section]['tabblock'][numBlock]['len'] = len


# while True:
#     sect = input(seccion)
#     if (sect):
#         varSECT = sect

# lexer = lex.lex()
# while True:
#     data = input("expression: ")
#     data2 = validateExSyntax(data)
#     if (data2 == True):
#         print("correct expresion :D")
#     else:
#         print("expression invalida sintacticamente: " + errorDescription)

################################################
   # lexer.input(data)

    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break
    #     print(tok)
#################################
print(validateExRelativity_A_R_I('4*(SALTO-ETIQ)+TAM+AFHH'))
