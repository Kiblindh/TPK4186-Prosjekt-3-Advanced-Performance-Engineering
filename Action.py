class Action:
    NONE = 0
    LOADFIRSTBUFFER = 1
    LOADTOTASK = 2
    DOTASK = 3 
    TASKDONE = 4
    
    def __init__(self, actionType, batch, startTime, completionTime, task = None, inputBuffer = None, outputBuffer = None):
        self.actionType = actionType
        self.batch = batch
        self.inputBuffer = inputBuffer
        self.outputBuffer = outputBuffer
        self.nextActionToDo = None
        self.task = task
        self.startTime = startTime
        self.completionTime = completionTime       
        self.controlAction = False
        
    def getActionType(self):
        return self.actionType
    
    def setActionType(self, actionType):
        self.actionType = actionType

    def getBatch(self):
        return self.batch
    
    def setBatch(self, batch):
        self.batch = batch
    
    def getInputBuffer(self):
        return self.inputBuffer
    
    def setInputBuffer(self, inputBuffer):
        self.inputBuffer = inputBuffer
    
    def getOutputBuffer(self):
        return self.outputBuffer
    
    def setOutputBuffer(self, outputBuffer):
        self.outputBuffer = outputBuffer
    
    def getNextActionToDo(self):
        return self.nextActionToDo
    
    def setNextActionToDo(self, nextAction):
        self.nextActionToDo = nextAction
    
    def getStartTime(self):
        return self.startTime
    
    def setStartTime(self, startTime):
        self.startTime = startTime

    def getCompletionTime(self):
        return self.completionTime
    
    def setCompletionTime(self, completionTime):
        self.completionTime = completionTime
    
    def getTask(self):
        return self.task
    
    def setTask(self, task):
        self.task = task

    def addTimeToAction(self, timeToAdd):
        self.startTime += timeToAdd
    
    def getControlAction(self):
        return self.controlAction

    def setControlAction(self, controlAction):
        if controlAction == True:
            self.controlAction = True
        elif controlAction == False:
            self.controlAction = False
        else:
            print("Invalid controlAction input")
            return None
