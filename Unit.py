# Imported modules
# --------------------
from Task import *
from Buffer import *
from Action import *

class Unit:
    def __init__(self, numberUnit):
        self.numberUnit = numberUnit
        self.tasks = []
        self.batches = []
        self.isUsed = False
        self.tasksInUnits = [1,3,6,9, 2,5,7, 4,8]  
    
    def getTasks(self):
        return self.tasks
    
    def setTasks(self, tasks):
        self.tasks = tasks
    
    def addTask(self, task):
        task.setUnitFromTask(self)
        self.tasks.append(task)
    
    def getNumberUnit(self):
        return self.numberUnit
    
    def setNumberUnit(self, numberUnit):
        self.numberUnit = numberUnit

    def getBatches(self):
        return self.batches
    
    def setBatches(self, batches):
        self.batches = batches

    def getTaskFromNmr(self, taskNmr):
        for task in self.tasks:
            if task.getTaskNmr() == taskNmr:
                return task
        return None
    
    def chooseBufferToProcess(self): # Sorts based off batch size in the accompanying buffers
        batchToTreat = 0
        chosenBuffer = 0
        for task in self.tasks:
            inputBuffer = task.getInputBuffer()
            firstBatchInBuffer = inputBuffer.getBatch(0)
            if task.canTaskRun(firstBatchInBuffer) == True:
                if firstBatchInBuffer.getBatchSize() > batchToTreat:
                    batchToTreat = firstBatchInBuffer.getBatchSize()
                    chosenBuffer = inputBuffer.getBufferNumber()
            else:
                pass
            
        if chosenBuffer == 0:
            print("No tasks for this unit can be performed until a buffer has cleared space")
            return None
        return chosenBuffer
    
    def updateTimes(self, startTime, completionTime, batch, task):
        startTime = completionTime
        completionTime = startTime + task.calculateTaskTime(batch)
        return startTime, completionTime
    
    def processActions(self, actionToLoad, actionToDo, actionTaskDone):
        actionToDo.setNextActionToDo(actionTaskDone)
        actionToLoad.setNextActionToDo(actionToDo)
        return actionToLoad, actionToDo, actionTaskDone

    def actionToStartUnit(self, startTime):
        #tasksInUnits = [[1,3,6,9], [2,5,7], [4,8]]
        for taskNmr in self.tasksInUnits:
            task = self.getTaskFromNmr(taskNmr)
            if task != None:
                inputBuffer = task.getInputBuffer()
                for batch in inputBuffer.getBatchesInBuffer():
                    if task.canTaskRun(batch):
                        completionTime = startTime + 1 #task.calculateTaskTime(batch)
                        actionToLoad = Action(Action.LOADTOTASK, batch, startTime, completionTime, task, inputBuffer)
                        startTime, completionTime = self.updateTimes(startTime, completionTime, batch, task)
                        actionToDo = Action(Action.DOTASK, batch, startTime, completionTime, task, None)
                        startTime, completionTime = self.updateTimes(startTime, completionTime, batch, task)
                        actionTaskDone = Action(Action.TASKDONE, batch, startTime, completionTime, task, None, task.getOutputBuffer())
                        
                        actionToLoad, actionToDo, actionTaskDone = self.processActions(actionToLoad, actionToDo, actionTaskDone)
                        return actionToLoad

    def setAvailable(self, status):
        if(status == False or status == True):
            self.isUsed = status
        else:
            raise Exception("The status of the unit has to be true or false")
    
    def isAvailable(self):
        if(self.isUsed == False):
            return True
        else:
            return False

    