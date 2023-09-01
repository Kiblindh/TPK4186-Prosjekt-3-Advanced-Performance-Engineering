# Imported modules
# ------------------------------
from ProdLine import *
from Action import *
from Scheduler import *
from ActionTracker import *

class Simulator:
    def __init__(self, prodLine, stopPoint):
        self.prodLine = prodLine
        self.scheduler = Scheduler()
        self.actionTracker = ActionTracker()
        self.printer = Printer(self.scheduler, self.actionTracker.getActionTracker())
        self.doneActions = Scheduler()
        self.stopPoint = stopPoint
        self.testPrinter = Printer(self.scheduler, self.actionTracker.getActionTracker())
        self.time = 0
        self.loadTime = 1

        # self.batchList = [Batch(1, 50)]
        self.batchList = self.prodLine.splitBaseLineWafersToBatches(50)
        # self.batchList = self.prodLine.splitRandomWafersToBatches(stopPoint)
        
    def getTime(self):
        return self.time
    
    def setTime(self, time):
        self.time = time

    def getScheduler(self):
        return self.scheduler
    
    def getScheduledActions(self):
        return self.scheduler.getActions()
    
    def getDoneActions(self):
        return self.doneActions
        
    def loadBatchToFirstBuff(self, batch): # Executes and loads the first buffer
        task, unit = self.prodLine.getTaskAndUnits(1)
        inputBuffer = task.getInputBuffer()
        startTime = self.time
        completionTime = self.time + self.loadTime
        loadAction = Action(Action.LOADFIRSTBUFFER, batch, startTime, completionTime, task, inputBuffer)
        self.scheduler.insertActionToScheduler(loadAction)
        loadAction.setControlAction(True) 
        actionProgress = "Batch: " + str(batch) + " loading to firstBuffer at " + str(loadAction.getStartTime())
        self.actionTracker.trackAction(self.time, actionProgress)
        
    def isSpaceInFirstBuff(self, batch):
        task, unit = self.prodLine.getTaskAndUnits(1)
        inputBuffer = task.getInputBuffer()
        return not inputBuffer.overLoadedBuffer(batch)
    
    def controlActionsInProcess(self): # Controls ongoing actions
        actions = self.scheduler.getActions()
        for action in actions:
            completionTime = action.getCompletionTime()
            if action.getControlAction() == True:
                if completionTime <= self.time:
                    self.completeActionInUnit(action)
    
    def generateActionForTasks(self): # Creates new actions
        units = self.prodLine.getUnits()
        for unit in units:
            if not unit.isAvailable():
                continue
            actionForTask = unit.actionToStartUnit(self.time)
            if actionForTask != None:
                self.scheduler.insertActionToScheduler(actionForTask)
                
    def generateActionForInputLoad(self): # Generates an action that loads the first inputBuffer
        tempBatchList = self.batchList
        for i in range(len(tempBatchList)):
            if self.isSpaceInFirstBuff(tempBatchList[i]):
                batch = self.batchList.pop(i)
                self.loadBatchToFirstBuff(batch)
                break

    def performActionsIn3Units(self): # Executes the actions to be performed
        actions = self.scheduler.getActions()
        if len(actions) != 0:
            units = self.prodLine.getUnits()
            for unit in units:
                if not unit.isAvailable():
                    continue
                for task in unit.tasksInUnits:
                    for action in actions:
                        taskFromAction = action.getTask()
                        if taskFromAction == None:
                            continue
                        if taskFromAction.getTaskNmr() == task:
                            self.performActionInUnit(unit, action)
    
    def performActionInUnit(self, unit, action):
        if action.getActionType() == Action.LOADTOTASK:
            unit.setAvailable(False)
            action.setControlAction(True)
            task = action.getTask()
            task.setTaskBusy(True)
            batch = action.getBatch()
            actionProgress = "Began batch: " +  str(batch.getBatchNumber()) + " to be loaded to task: " + str(task.getTaskNmr()) + " at: " + str(action.getStartTime())
            self.actionTracker.trackAction(self.time, actionProgress)
        
        elif action.getActionType() == Action.DOTASK:
            batch = action.getBatch()
            task = action.getTask()
            actionProgress = "Began batch being processed: " +  str(batch.getBatchNumber()) + " in task: " + str(task.getTaskNmr()) + " at: " + str(action.getStartTime())
            self.actionTracker.trackAction(self.time, actionProgress)
            action.setControlAction(True)
        
        elif action.getActionType() == Action.TASKDONE:
            batch = action.getBatch()
            task = action.getTask()
            actionProgress = "Began batch being unloaded: " +  str(batch.getBatchNumber()) + " to task: " + str(task.getTaskNmr()) + " at: " + str(action.getStartTime())
            self.actionTracker.trackAction(self.time, actionProgress)
            action.setControlAction(True)
        
    def completeActionInUnit(self, action): # Finishes the actions performed earlier
        noUnit = None
        if action.getActionType() == Action.LOADFIRSTBUFFER:
            # ----------- Variables: --------------
            batch = action.getBatch()
            inputBuffer = action.getInputBuffer()
            task = action.getTask()
            # ----------- Actual actions to run the prodLine: --------------
            inputBuffer.loadBuffer(batch) 
            self.scheduler.removeActionFromScheduler(action)
            actionProgress = "Batch: " + str(batch) + " placed in inputBuffer: " + str(inputBuffer.getBufferNumber()+1) + " at: " + str(action.getCompletionTime())
            self.actionTracker.trackAction(self.time, actionProgress)
        
        elif action.getActionType() == Action.LOADTOTASK:
            # ----------- Variables: --------------
            inputBuffer = action.getInputBuffer()
            task = action.getTask()
            batch = action.getBatch()
            # ----------- Actual actions to run the prodLine: --------------
            inputBuffer.unloadBufferByBatch(batch)
            nextAction = action.getNextActionToDo()
            self.scheduler.removeActionFromScheduler(action)
            self.scheduler.insertActionToScheduler(nextAction)
            self.performActionInUnit(noUnit, nextAction)
            actionProgress = "Batch: " + str(batch) + " placed in task: " + str(task.getTaskNmr() + 1) + " at: " + str(action.getCompletionTime())
            self.actionTracker.trackAction(self.time, actionProgress)

        elif action.getActionType() == Action.DOTASK:
            # ----------- Variables: --------------
            nextAction = action.getNextActionToDo()
            task = action.getTask()
            batch = action.getBatch()
            # ----------- Actual actions to run the prodLine: --------------
            self.scheduler.removeActionFromScheduler(action)
            self.scheduler.insertActionToScheduler(nextAction)
            self.performActionInUnit(noUnit, nextAction)
            actionProgress = "Batch: " + str(batch) + " processed in task: " + str(task.getTaskNmr() + 1) + " at: " + str(action.getCompletionTime())
            # self.performAction(unit, action)
            self.actionTracker.trackAction(self.time, actionProgress)

        elif action.getActionType() == Action.TASKDONE:
            # ----------- Variables: --------------
            task = action.getTask()
            unit = task.getUnitFromTask()
            batch = action.getBatch()
            # ----------- Actual actions to run the prodLine: --------------
            self.scheduler.removeActionFromScheduler(action)
            unit.setAvailable(False)
            outputBuffer = action.getOutputBuffer()
            outputBuffer.loadBuffer(batch)
            actionProgress = "Batch: " + str(batch) + " loaded to outputBuffer " + str(outputBuffer.getBufferNumber()) +  " in unit: " + str(unit.getNumberUnit()) + " at: " + str(action.getCompletionTime())
            self.actionTracker.trackAction(self.time, actionProgress)

    def simDone(self):
        lastBuffer = self.prodLine.getBuffer(9)
        wafers = lastBuffer.getSizeOfAllBatches()
        if wafers == self.stopPoint and len(self.scheduler.getActions())==0:
            return True
        return False

    def simulationLoop(self):
        count = 0
        fileName = "Simulation.txt"
        self.testPrinter.wipeFile(fileName)
        while self.simDone() != True:

            self.controlActionsInProcess()
            self.generateActionForTasks()
            self.performActionsIn3Units()
            self.generateActionForInputLoad()

            self.testPrinter.printSchedule(self.getTime(), fileName)
            
            if not self.scheduler.isEmpty():
                self.time = self.time + 1
                count += 1
            
        self.testPrinter.printFinal(self.getTime(), fileName)
        print("Count: ", count)
