#Generate a csv with all the data colected
#Répéterpour plusieurs itération ce qu'a fait la meilleur fusée pour avoir un résultat moyen fusée 
#Faire un test avec des fusée lancer au hasard 
#Faire un test aec des fusées qui allument leur booster une fois sur deux

import pandas as pd
import re
import numpy as np
from numpy import array

class RocketData:
    
    def __init__(self,data = [1] ,weights = [1]):
        
        
        self.identifier = data[2]
        self.v_final = data[3]
        self.altitude = data[4]
        self.fuel_left = data[5]
        self.fitness = data[1]
        self.weights = np.array_repr(np.array(weights))
        # Pour le récupérer  arr = eval(self.weights)        

    def write_info(self):
        data = [
            self.identifier,
            self.v_final,
            self.altitude,
            self.fuel_left,
            self.fitness,
            self. weights
        ]

        #DECOMPOSER LES POIDS EN VALEURS COMPREHESIBLE
        formatedData = pd.DataFrame.from_dict(data, orient='columns', dtype=None, columns=None)

        formatedData.to_csv('data/'+re.findall(r'\d+\.?[\d]+?',self.identifier)[0]+'.csv', encoding='utf-8', index= False)
        

    def get_info(self,indentifier):
        """
            On cherche à l'aide de l'identifiant la fusée désiré 
            On set toute les valeur d'interêt
        """
        pass        

    
