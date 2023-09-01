# 1. Imported modules
# ------------------------------------------
from Batch import *
from Buffer import *
from Printer import *
from ProdLine import *
from Simulator import *
from Optimization import *

# 2. Global variables
# --------------------------------------------

optimization = Optimization()
fileName = "test.txt"




#-----------------------------------
# Test Simulator
#-----------------------------------

# Test for one batch of 50 wafers: 
'''prodLine = ProdLine()
prodLine.createProdLine()

stopPoint = 50
simulator1 = Simulator(prodLine, stopPoint)

simulator1.simulationLoop()
scheduler = simulator1.getScheduler()
actions = scheduler.getActions()
'''
# Test for 25 batches of in total 1000 wafers:
prodLine = ProdLine()
prodLine.createProdLine()

stopPoint = 1000
simulator1 = Simulator(prodLine, stopPoint)

simulator1.simulationLoop()
scheduler = simulator1.getScheduler()
actions = scheduler.getActions()