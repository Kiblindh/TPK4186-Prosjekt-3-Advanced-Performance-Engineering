# 1. Imported Modules
# -------------------
import numpy as np
# import random
import inspect
import matplotlib.pyplot as plt

class Optimization:
    def __init__(self):
        return
    
    def PlotSimulationTimes(self, simulations):
        simulationNumber = list(range(1, len(simulations)+1))
        time = [elem[0] for elem in simulations]
        
        fig = plt.figure(figsize = (11, 5))
        # creating the bar plot
        plt.plot(simulationNumber, time, color ='burlywood')
        plt.xlabel("Simulation number")
        plt.ylabel("Time [in units] for each simulation")
        frame = inspect.currentframe()
        plt.xticks(np.arange(1, len(simulations)+1))
        name = [key for key, value in frame.f_back.f_locals.items() if value is simulations][0]
        plt.title(f"Optimization: {name}")
         #plt.savefig('plots/' + simulations + ".png")
        plt.show()

