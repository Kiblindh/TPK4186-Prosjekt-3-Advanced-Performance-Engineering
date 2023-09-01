class Printer:
    def __init__(self, scheduler, actionTracker ):
        self.scheduler = scheduler
        self.actionTracker = actionTracker
    
    def printBatches(self, batches):
        for batch in batches:
            print("Batch number:", batch.getBatchNumber(), " Size:", batch.getBatchSize())
    
    def printBuffers(self, buffers):
        for buffer in buffers:
            print("Buffer number: ", buffer.getBufferNumber())
    
    def printProdLine(self, prodLine):
        units = prodLine.getUnits()
        for unit in units:
            print("Unit: ", unit.getNumberUnit(), " has these tasks: ")
            tasks = unit.getTasks()
            for task in tasks:
                print("\tTask: ", task.getTaskNmr(), " has these buffers: ")
                print("\t\tInput: ", task.getInputBuffer().getBufferNumber(), " Output: ", task.getOutputBuffer().getBufferNumber())

    def printBatch(self, batch, outputFile):
        outputFile.write("{0:d}".format(batch.getBatchNumber()))
        outputFile.write(self.separator)
        outputFile.write("{0:d}".format(batch.getBatchSize()))
        outputFile.write(self.separator)
        
    def printActionType(self, action):
        str = None
        if action.getActionType() == 1:
            str = "LOADFIRSTBUFFER"
        elif action.getActionType() == 2:
            str = "LOADTOTASK"
        elif action.getActionType() == 3:
            str = "DOTASK"
        elif action.getActionType() == 4:
            str = "TASKDONE"
        else:
            str = None
        return str
    
    def printAction(self, action, outputFile):
        outputFile.write(action)
        outputFile.write("\n")

    def printFinal(self, time, fileName):
        outputFile = open(fileName, "a")
        outputFile.write("Simulation done at: " + str(time))
        outputFile.close()

    def wipeFile(self, fileName):
        with open(fileName,'w') as file:
            pass

    def printSchedule(self, time, fileName):
        ok = True
        try:
            outputFile = open(fileName, "a")
        except:
            ok = False
        if ok:
            timesInTracker = self.actionTracker.keys()
            for timeIn in timesInTracker:
                if timeIn == time:
                    for action in self.actionTracker[time]:
                        outputFile.write("Action: " + str(action) + "\n")

            outputFile.close()

    def printOrderOfDoneBatches(self, simulator):
        for i in range(0, simulator.prodLine.getBuffers()[-1].getNumOfBatches()):
            print(print(simulator.prodLine.getBuffers()[-1].getBatch(i)))