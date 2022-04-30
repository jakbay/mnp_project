#fitness evolution over generation
#altitude if one rocket (so simulation with the best one)
#vitesse graph if one rocket
#fuel graph if one rocket
import matplotlib
matplotlib.use("Agg")
import pygame
import pandas as pd


class GraphHandler:

    def __init__(self):
       self.fitnessHistory = []
       
    def save_fitness(self):
        data = {
            "fitness" : self.fitnessHistory
        }
        formatedData = pd.DataFrame.from_dict(data, orient='columns', dtype=None, columns=None)

        formatedData.to_csv('data/oneovertwo.csv', encoding='utf-8', index= False)
    