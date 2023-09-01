class Batch:
    def __init__(self, batchNumber, batchSize):
        if batchSize < 20 or batchSize > 50:
            raise Exception("The batch size is smaller than 20 or bigger than 50")
        self.batchSize = batchSize
        self.batchNumber = batchNumber

    def getBatchNumber(self):
        return self.batchNumber
    
    def setBatchNumber(self, batchNumber):
        self.batchNumber = batchNumber
    
    def getBatchSize(self):
        return self.batchSize

    def setBatchSize(self, batchSize):
        self.batchSize = batchSize

    def __str__(self):
        return "Batch number: " + str(self.batchNumber) + ", Size: " + str(self.batchSize)
