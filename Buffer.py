# Imported modules
# ----------------------
from Task import *

class Buffer:
    def __init__(self, bufferNumber):
        self.batchesInBuffer = [] 
        self.bufferNumber = bufferNumber
        self.waferCount = 0

    def getBufferNumber(self):
        return self.bufferNumber

    def setBufferNumber(self, bufferNumber):
        self.bufferNumber = bufferNumber

    def unloadBufferByTask(self, task):
        if len(self.batchesInBuffer) == 0:
            print("Buffer empty")
            return None
        task.setBatch(self.batchesInBuffer[0])
        self.batchesInBuffer.pop(0)
        self.totalTime += 1 

    def loadBuffer(self, batch):
        self.overLoadedBuffer(batch)
        self.batchesInBuffer.append(batch)
        self.waferCount += batch.getBatchSize()
    
    def unloadBufferByBatch(self, batchToUnload):
        for batch in self.batchesInBuffer:
            if batch == batchToUnload:
                self.waferCount -= batchToUnload.getBatchSize()
                self.batchesInBuffer.remove(batch)
                return
        print("No such batch found")
        return None
    
    def isLastBuffer(self):
        if self.getBufferNumber() == 9:
            return True
        else:
            return False

    def getBatchesInBuffer(self):
        return self.batchesInBuffer
        
    def getBatch(self, bufferIndex): 
        return self.batchesInBuffer[bufferIndex]

    def getNumOfBatches(self):
        return len(self.batchesInBuffer)

    def getSizeOfAllBatches(self):
        batchesCount = 0
        for batch in self.getBatchesInBuffer():
            batchesCount += batch.getBatchSize()
        return batchesCount

    def overLoadedBuffer(self, batch):
        if(self.getSizeOfAllBatches() + batch.getBatchSize() > 120):
            return True
        elif(self.getNumOfBatches() + batch.getBatchSize() >= 1000 and self.isLastBuffer() == True):
            return False
        elif self.isLastBuffer() == True:
            return False
        else:
            return False