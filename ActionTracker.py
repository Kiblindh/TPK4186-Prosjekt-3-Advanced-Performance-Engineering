class ActionTracker:
    def __init__(self):
        self.actionTracker = dict()
    
    def getActionTracker(self):
        return self.actionTracker
    
    def trackAction(self, time, actionProgress):
        # Works as an addToActionTracker function
        
        if self.isTimeInTracker(actionProgress) != None:
            self.actionTracker[time].append(actionProgress)
        else:
            self.actionTracker[time] = [actionProgress]
        
    def isTimeInTracker(self, time):
        return self.actionTracker.get(time, None)