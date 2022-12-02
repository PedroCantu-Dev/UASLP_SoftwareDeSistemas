import calc.calc as calc


memory = {}


def cleanMemory(dirCounter=0):
    global memory
    memory = {}
    dirCounter = int(dirCounter/16)
    dirCounter = int(dirCounter * 16)
    for i in range(int((2**20)/16)):
        memoryRow = []
        for j in range(16):
            memoryRow.append('FF')
        memory[calc.SIC_HEX(dirCounter)] = memoryRow
        dirCounter += 16


def readAllocation(dir, bytes=3):
    global memory
    modDiv16 = calc.getIntBy_SicXe_HexOrInt(calc.SIC_HEX(dir)) % 16
    if modDiv16 == 0:
        memory[calc.SIC_HEX(dir)]


def writeAllocation(content, dir, dirRel=0):
    dir = calc.getIntBy_SicXe_HexOrInt(
        dir, True) + calc.getIntBy_SicXe_HexOrInt(dirRel, True)
    allocationColumn = dir % 16
    allocation = dir - allocationColumn
    content = splitEachTwo(content)
    rowCounter = 1
    while (True):
        row = memory[calc.SIC_HEX(allocation)]
        for i in range(len(content)):
            if (allocationColumn > 15):
                allocation += 16
                allocationColumn = 0
                row = memory[calc.SIC_HEX(allocation)]
                row[allocationColumn] = content[i]
                rowCounter += 1
            else:
                row[allocationColumn] = content[i]
            i += 1
            allocationColumn += 1
        break
    return rowCounter


def writeAllocationR(content, dir, dirRel=0):
    dir = calc.getIntBy_SicXe_HexOrInt(
        dir, True) + calc.getIntBy_SicXe_HexOrInt(dirRel, True)
    contentAux = calc.SIC_HEX(content, len(content))
    dirAux = dir + int(len(contentAux)/2)

    allocationColumn = dirAux % 16
    allocation = dirAux - allocationColumn
    contentAux2 = splitEachTwoR(contentAux)
    rowCounter = 1
    while (True):
        memAlloc = calc.SIC_HEX(allocation)
        row = memory[memAlloc]
        for i in range(len(contentAux2)-1, -1, -1):
            if (allocationColumn < 0):
                allocation -= 16
                allocationColumn = 15
                memAlloc = calc.SIC_HEX(allocation)
                row = memory[memAlloc]
                row[allocationColumn] = contentAux2[i]
                rowCounter += 1
            else:
                row[allocationColumn] = contentAux2[i]
            allocationColumn -= 1
        break
    return rowCounter


def getAllocationRow(dir, dirRel=0):
    dir = calc.getIntBy_SicXe_HexOrInt(
        dir, True) + calc.getIntBy_SicXe_HexOrInt(dirRel, True)
    allocationColumn = dir % 16
    allocation = dir - allocationColumn
    return memory[calc.SIC_HEX(allocation)]


def readAllocation(dir, dirRel=0, medBytes=2, returnOdd=False):
    oddBool = False
    if (medBytes % 2 == 0):
        bytes = medBytes/2
    else:
        bytes = (medBytes+1)/2
        oddBool = True
    bytes = int(bytes)

    dir = calc.getIntBy_SicXe_HexOrInt(
        dir, True) + calc.getIntBy_SicXe_HexOrInt(dirRel, True)
    allocationColumn = dir % 16
    allocation = dir - allocationColumn
    content = ''

    while (True):
        row = memory[calc.SIC_HEX(allocation)]
        for i in range(bytes):
            if (allocationColumn > 15):
                allocation += 16
                allocationColumn = 0
                row = memory[calc.SIC_HEX(allocation)]
                content += row[allocationColumn]
            else:
                content += row[allocationColumn]
            i += 1
            allocationColumn += 1
        break
    if (oddBool and returnOdd):
        return content[1:]
    else:
        return content


def splitEachTwo(line, step=2):
    return [calc.SIC_HEX(line[i:i+step], step) for i in range(0, len(line), step)]


def splitEachTwoR(line, step=2):
    count = len(line)
    res = []
    step = step*-1
    lastInLine = line[count-1:]
    for i in range(count, -1, step):
        if (i+step <= step):
            break
        if (i+step > -1):
            res.append(calc.SIC_HEX(line[i+step:i], 2))
        else:
            res.append(calc.SIC_HEX(line[0:1], 2))
    return res[::-1]
    # return [try: calc.SIC_HEX(line[i:i+step], 2) except:pass for i in range(len(line)-1, -2, step)]


#######################
# Zona de pruebas
###################

# cleanMemory()
# # # writeAllocation('000037', '0FFAAA')
# writeAllocation('FFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', '000037',)
# writeAllocationR(
#     'BDDBBAAAADDEEBC', '3C')
# writeAllocation(
#     '42', 'aabb123456789ABCDEF123456789101112131415FEDCBA')
# pass
