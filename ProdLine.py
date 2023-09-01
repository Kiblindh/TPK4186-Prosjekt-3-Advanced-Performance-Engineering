# Imported modules
# ----------------------
import random
from Buffer import *
from Task import *
from Unit import *
from Printer import *

class ProdLine:
    def __init__(self):
        self.units = []
        self.buffers = []
    
    def getBuffers(self):
        return self.buffers

    def getBuffer(self, bufferNumber):
        for buffer in self.buffers:
            if bufferNumber == buffer.getBufferNumber():
                return buffer
        return None
    
    def getAllWaifersInProdLine(self):
        batchesCount = 0
        for buffer in self.buffers:
            batchesCount += buffer.getSizeOfAllBatches()
        return batchesCount

    def getUnits(self):
        return self.units
    
    def setUnits(self, units):
        self.units = units

    def createProdLine(self):
        self.generateBufferList()
        for i in range(3):
            unit = self.generateUnit(i+1)
            self.units.append(unit)

    def generateBufferList(self):
        for i in range(10):
            if i == 9:
                lastBuffer = Buffer(i)
                lastBuffer.isLastBuffer()
                self.buffers.append(lastBuffer)
            else:
                self.buffers.append(Buffer(i))

    def generateUnit(self, unitNumber):
        unit = Unit(unitNumber)
        tasksInUnits = [[1,3,6,9], [2,5,7], [4,8]]  
        for element in tasksInUnits[unitNumber-1]:
            task = self.generateTask(element)
            unit.addTask(task)
        return unit
    
    def generateTask(self, taskNmr):
        task = Task(taskNmr, inputBuffer=self.buffers[taskNmr-1], outputBuffer=self.buffers[taskNmr])
        return task
    
    def getTaskAndUnits(self, taskNmr):
        unit = Unit(0)
        Units = self.getUnits()
        wantedTask = None
        if(taskNmr in [1,3,6,9]):
            unit = Units[0]
        elif(taskNmr in [2,5,7]):
            unit = Units[1]
        elif(taskNmr in [4,8]):
            unit = Units[2]
        for task in unit.getTasks():
            if(task.getTaskNmr() == taskNmr):
                wantedTask = task
        return wantedTask, unit

    def splitRandomWafersToBatches(self, numWafers):
        numCount = 0
        batchList = []
        while numWafers != 0:
            if numWafers <= 50 and numWafers > 20 or numWafers < 50 and numWafers >= 20:
                batch = Batch(numCount, numWafers)
                batchSize = batch.getBatchSize()
                batchList.append(batch)
                numWafers -= batchSize
                break

            batchSize = random.randint(20,50)
            while numWafers - batchSize < 20:
                batchSize = random.randint(20,50)
            batch = Batch(numCount, batchSize)
            batchList.append(batch)
            numWafers -= batchSize
            numCount += 1
        
        return batchList
    
    def splitBaseLineWafersToBatches(self, numWafersInBatch):
        numCount = 0
        batchList = []
        numWafers = 1000
        if numWafersInBatch <= 50 and numWafersInBatch >= 20:
            while numWafers != 0:
                if numWafers - numWafersInBatch <= 0: 
                    batch = Batch(numCount, numWafers)            
                    batchSize = numWafers
                    batchList.append(batch)
                    numWafers -= batchSize                  
                    break
                elif numWafers - numWafersInBatch == 0:
                    batch = Batch(numCount, numWafers) 
                    batchSize = numWafersInBatch
                    batchList.append(batch)
                    numWafers -= batchSize
                    break
                elif numWafers - numWafersInBatch > 0 and (numWafers <= numWafersInBatch or numWafers < 50):
                    if numWafers + numWafersInBatch >= 50:
                        batch = Batch(numCount, numWafers) 
                        batchSize = int((numWafers + numWafersInBatch)/2)
                        batchList.append(batch)
                        numWafers -= batchSize
                        break
                    else:
                        batch = Batch(numCount, numWafers) 
                        batchSize = numWafers + numWafersInBatch
                        batchList.append(batch)
                        numWafers -= batchSize
                        break
                batchSize = numWafersInBatch
                batch = Batch(numCount, batchSize)
                batchList.append(batch)
                numWafers -= batchSize
                numCount += 1
            return batchList
        else:
            raise Exception("The batch size is not valid")