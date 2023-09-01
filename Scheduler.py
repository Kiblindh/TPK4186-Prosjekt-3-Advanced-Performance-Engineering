from Action import *
from ProdLine import *

class Scheduler:
    def __init__(self):
        self.actions = []
        self.completedActions = []
    
    def getActions(self):
        return self.actions
    
    def setActions(self, actions):
        self.actions = actions

    def getNumberOfActions(self):
        return len(self.actions)
	
    def isEmpty(self):
        return len(self.actions)==0
    
    def insertActionToScheduler(self, action):
        self.actions.append(action)
    
    def removeActionFromScheduler(self, action):
        self.actions.remove(action)
    
    def popFirstAction(self):
        if self.isEmpty():
            return None
        return self.actions.pop(0)
    
    
