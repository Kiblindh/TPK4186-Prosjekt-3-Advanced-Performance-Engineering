# Imported modules
# --------------------
from Batch import *

processingTime = {1:0.5, 2:3.5, 3:1.2, 4:3, 5:0.8, 6:0.5, 7:1, 8:1.9, 9:0.3}

class Task:
    def __init__(self, taskNmr, inputBuffer, outputBuffer):
        self.taskNmr = taskNmr
        self.inputBuffer = inputBuffer
        self.outputBuffer = outputBuffer
        self.batch = None
        self.taskTime = None
        self.unitFromTask = None
        self.taskBusy = False

    def getTaskNmr(self):
        return self.taskNmr
    
    def setTaskNmr(self, taskNmr):
        if taskNmr<0 or taskNmr>9:
            print("Task number must be between 0 and 9")
            return None
        self.taskNmr = taskNmr

    def getInputBuffer(self):
        return self.inputBuffer
    
    def setInputBuffer(self, inputBuffer):
        self.inputBuffer = inputBuffer

    def getOutputBuffer(self):
        return self.outputBuffer
    
    def setOutputBuffer(self, outputBuffer):
        self.outputBuffer = outputBuffer
    
    def getBatch(self):
        return self.batch
    
    def setBatch(self, batch):
        self.batch = batch

    def getTaskTime(self):
        return self.taskTime

    def getUnitFromTask(self):
        return self.unitFromTask

    def setUnitFromTask(self, unitFromTask):
        self.unitFromTask = unitFromTask
    
    def getTaskBusy(self):
        return self.taskBusy
    
    def setTaskBusy(self, taskBusy):
        if taskBusy == True:
            self.taskBusy = True
        elif taskBusy == False:
            self.taskBusy = False
        else:
            print("Invalid entry for status")
            return None
    
    def calculateTaskTime(self, batch):
        wafers = batch.getBatchSize()
        taskTime = wafers * processingTime[self.taskNmr]
        self.taskTime = taskTime
        return taskTime

    def canTaskRun(self, nextBatch):
        outputBuff = self.outputBuffer
        batches = outputBuff.getBatchesInBuffer()
        wafers = 0
        for batch in batches:
            wafers += batch.getBatchSize()
        if (wafers + (nextBatch.getBatchSize())) > 120: 
            return False
        return True
