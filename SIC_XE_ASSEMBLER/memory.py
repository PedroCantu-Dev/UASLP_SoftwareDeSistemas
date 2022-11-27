import calc.calc as calc

memory = {}


def cleanMemory():
    global memory
    memory = {}
    dirCounter = 0
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


def getAllocationRow(dir, dirRel=0):
    dir = calc.getIntBy_SicXe_HexOrInt(
        dir, True) + calc.getIntBy_SicXe_HexOrInt(dirRel, True)
    allocationColumn = dir % 16
    allocation = dir - allocationColumn
    return memory[calc.SIC_HEX(allocation)]


def splitEachTwo(line, step=2):
    return [calc.SIC_HEX(line[i:i+step], 2) for i in range(0, len(line), step)]


#######################
# Zona de pruebas
###################

# cleanMemory()
# # writeAllocation('000037', '0FFAAA')
# # writeAllocation('000037', 'FFAAAA')
# writeAllocation(
#     '42', 'aabb123456789ABCDEF123456789101112131415FEDCBA')
# pass
