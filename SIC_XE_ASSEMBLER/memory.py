import calc.calc as calc


def getCleanMemory():
    memory = {}
    dirCounter = 0
    for i in range(int((2**20)/15)):
        memoryRow = []
        for j in range(16):
            memoryRow.append('FF')
        memory[calc.SIC_HEX(dirCounter)] = memoryRow
        dirCounter += 16
    pass


getCleanMemory()
