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


def writeAllocation(dir, operand):
    pass


def getAllocationRow(allocation):
    return memory[allocation]


cleanMemory()
