import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dataFitness = pd.read_csv('data/fitnessHistory.csv')
dataFitness = dataFitness.values.tolist()
reformatedFitness = []

for i in range(len(dataFitness)):
    reformatedFitness.append(dataFitness[i][0])

generation = np.arange(1,len(reformatedFitness)+1,1)
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.plot(generation,reformatedFitness)
plt.show()