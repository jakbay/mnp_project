import random 
import math

class Genome:
    def __init__(self,agents,fitnessArr):
        self.newGeneration = []
        self.selection(agents,fitnessArr)
        self.crossover(agents)
        #self.mutate() 

    def selection(self,agents,fitnessArr):
        for i in range(len(fitnessArr)):
            self.newGeneration.append(agents[fitnessArr[i][0]])

    def crossover(self,agents):
        
        for i in range(3):
            for z in range(10):
                if(z < 9):
                    parent1 = self.newGeneration[z]
                    parent2 = self.newGeneration[z+1]
                    newAI = AI()
                    for i in range(2):
                        for j in range(6):
                            if random.uniform(0,1) > 0.5:
                                newAI.weights[i][j] = parent1.weights[i][j] 
                            else:
                                newAI.weights[i][j] = parent2.weights[i][j] 
                    self.newGeneration.append(newAI)
        for i in range(3):
            for z in range(10,len(self.newGeneration)):
                if(z < 19):
                    parent1 = self.newGeneration[z]
                    parent2 = self.newGeneration[z+1]
                    newAI = AI()
                    for i in range(2):
                        for j in range(6):
                            if random.uniform(0,1) > 0.5:
                                newAI.weights[i][j] = parent1.weights[i][j] 
                            else:
                                newAI.weights[i][j] = parent2.weights[i][j] 
                    self.newGeneration.append(newAI)
        
        ran = random.choices(agents, k=26)
        self.newGeneration.extend(ran)
    def mutate():
        pass

class AI:
    def __init__(self,weights = False):
        self.output = False
        self.y = 0
        self.v_final = 0
        self.rocket_mass = 0
        if weights :
            self.weights = weights
        else:
            self.weights = [
                [
                    [random.uniform(-1,1),random.uniform(-1,1)],
                    [random.uniform(-1,1),random.uniform(-1,1)],
                    [random.uniform(-1,1),random.uniform(-1,1)],
                    [random.uniform(-1,1),random.uniform(-1,1)],
                    [random.uniform(-1,1),random.uniform(-1,1)],
                    [random.uniform(-1,1),random.uniform(-1,1)],
                ],
                [
                    random.uniform(-1,1),
                    random.uniform(-1,1),
                    random.uniform(-1,1),
                    random.uniform(-1,1),
                    random.uniform(-1,1),
                    random.uniform(-1,1)
                ]
            ]

    def getOutput(self,input1,input2):
        transit_neurone_value = []
        output = 0
        for i in range(5):
            transit_neurone_value.append(self.sigmoid(self.weights[0][i][0]*float(input1) +self.weights[0][i][1])*float(input2))
        for i in range(5):
            output += (float(self.weights[1][i]) * float(transit_neurone_value[i]))

        self.output = self.sigmoid(output) > 0.5
        return (self.sigmoid(output) > 0.5)

    def sigmoid(self,input):
        if input < 0:
            return 1 - 1/(1 + math.exp(input))
        else:
            return 1/(1 + math.exp(-input))

    def fitnessCalc(self):
        return (1/(self.v_final + self.y) + self.fuel_left*1e-6)

class Neat:
    def __init__(self,POPULATION_SIZE,GENERATION_COUNT):
        self.GENERATION_COUNT = GENERATION_COUNT
        self.POPULATION_SIZE = POPULATION_SIZE
        self.agents = []
        self.fitnessArr = []
        self.BestAgent = AI() 
    
    def init_first_generation(self):
        for i in range(self.POPULATION_SIZE):
            self.agents.append(AI())
        

    def stop_generation(self,signal = False):
        for i in range(self.POPULATION_SIZE):
            self.fitnessArr.append((i,self.agents[i].fitnessCalc()))
        
        self.fitnessArr.sort(key = lambda x: x[1])

        genome = Genome(self.agents,self.fitnessArr[-20:])

        #print("Five best score : ", self.fitnessArr[-3:])

        self.agents = genome.newGeneration

        if signal:
            best = self.agents[self.fitnessArr[99][0]]
            self.agents = []
            for i in range(100):
                self.agents.append(best)
            print(best.v_final*36,"km/h vitesse final")
            print(best.y,"m altitude finale")

        self.fitnessArr = []