
def run(p):
    if type(p) == tuple:
        tupleValues = p.value
        firstElement = tupleValues[0]
        if(firstElement == 'programa'):
            programInicio = run(tupleValues[1])
            programProposiciones = run(tupleValues[2])
            programFin = run(tupleValues[3])
            print(programInicio + '\n' +
                  programProposiciones + '\n' + programFin)
        elif firstElement == 'inicio':
            programName = run(tupleValues[1])
            startToken = run(tupleValues[2])
            startAddressString = str(run(tupleValues[3]))
            # linea start
            lineSTART = programName.value + ';' + startToken + ';' + startAddressString
            return lineSTART
        elif firstElement == 'error_inicio_nombre_programa':
            startToken = run(tupleValues[2])
            startAddressString = str(run(tupleValues[3]))
            # linea start
            lineSTART = programName.type + ';' + startToken + ';' + startAddressString
            return lineSTART
        elif firstElement == 'error_inicio_numero':
            programName = run(tupleValues[1])
            startToken = run(tupleValues[2])
            startAddressString = run(tupleValues[3])
            # linea start
            lineSTART = programName.type + ';' + startToken + ';' + startAddressString
            return lineSTART
        elif firstElement == 'numero':
            if(tupleValues[1].type == 'HEX_INT'):
                return 'HEX_INT'
            elif(tupleValues[1].type == 'INT'):
                return 'INT'
            else:
                return 'NULL_numero'
        elif firstElement == 'fin':
            return 'END' + ' ' + run(tupleValues[1])
        elif firstElement == 'entrada':
            return run(tupleValues[1])
        elif firstElement == 'f1':
            return run(tupleValues[1])
        elif firstElement == 'f2':
            return run(tupleValues[1])
        elif firstElement == 'f3':
            return run(tupleValues[1])
        elif firstElement == 'f3,X':
            return run(tupleValues[1]) + run(tupleValues[2]) + run(tupleValues[3])
        elif firstElement == 'proposiciones-multi':
            return run(tupleValues[1]) + run(tupleValues[2])
        elif firstElement == 'proposiciones':
            return run(tupleValues[1])
        elif firstElement == 'proposicion':
            return run(tupleValues[1])
        elif firstElement == 'directiva':
            return run(tupleValues[1])
        elif firstElement == 'instruccion':
            return run(tupleValues[1])
        elif firstElement == 'error':
            return run(tupleValues[1])
        elif firstElement == 'opformato':
            return run(tupleValues[1])
        elif firstElement == 'simple3':
            print("simple3")
            return run(tupleValues[1]) + ' ' + run(tupleValues[2])
        elif firstElement == 'indirecto3':
            print("indirecto3:")
            return run(tupleValues[1]) + ' ' + run(tupleValues[2]) + run(tupleValues[3])
        elif firstElement == 'inmediato3':
            print("inmediato3:")
            return run(tupleValues[1])
        elif firstElement == 'RSUB':
            print("RSUB")
            return run(tupleValues[0])
            # parte de la calculadora de expresiones
        elif p[0].value == '+':
            return run(p[1]) + run(p[2])
        elif p[0].value == '-':
            return run(p[1]) - run(p[2])
        elif p[0].value == '*':
            return run(p[1]) * run(p[2])
        elif p[0].value == '/':
            divisor = run(p[2])
            if(divisor > 0):
                return run(p[1]) / run(p[2])
            else:
                return inf
        elif p[0].value == '%':
            return run(p[1]) % run(p[2])
        elif p[0].value == '||':
            if(run(p[1]) > 0 or run(p[2]) > 0):
                return 1
            else:
                return 0
        elif p[0] == '&&':
            if(run(p[1]) > 0 and run(p[2]) > 0):
                return 1
            else:
                return 0
        elif p[0] == '<':
            if(run(p[1]) < run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '>':
            if(run(p[1]) > run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '<=':
            if(run(p[1]) <= run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '>=':
            if(run(p[1]) >= run(p[2])):
                return 1
            else:
                return 0
        elif p[0] == '=':
            env[p[1]] = run(p[2])
            return env[p[1]]
        elif p[0] == 'uminus':
            print("funciono muminus")
            return -(run(p[1]))
        elif p[0] == 'var':
            return env[p[1]]
        elif p[0] == '!':
            return math.factorial(int(run(p[1])))
    else:
        print(p)
        if(p.type == 'etiqueta'):
            print(p.value.value)
            print(p.value.lineno)
            print(p.value.lexpos)
        elif(p.type == 'directiva'):
            {}
        elif(p.type == 'directiva'):
            {}
        elif(p.type == 'nombre_programa'):
            {}
        elif(p.type == 'directiva'):
            {}
        elif(p.type == 'directiva'):
            {}
        return p.value


def runApropiate(objX):
    if(objX == tuple()):
        for elemento in objX:
            if(hasattr(objX, 'value')):
                return(run(objX.value))
            else:
                return
