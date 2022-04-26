import random 
import math
from itertools import combinations
import numpy as np

SELECTION_SIZE = 17
STAGNATION = 5
PRESERVE_NB = 5
NEWBLOOD_SIZE = 1
DISPLAY_SCORES = 25
# CH nb must be par
CHROMOSOMES_LAYER_WIDTH = 10
CHROMOSOMES_LAYER_NB = 3
MAX_MUTATION_RATE = 0.99 # ratio
MAX_MUTATIONS = 10 # ratio
V_MAX_TOUCHDOWN = 0.1 # m/s
HEIGHT = 0
t = 0
current_id = 0
GENERATION_COUNT = 0
best_score = 0
last_best_score = 0
best_score_count = 0

class Genome:
    def __init__(self,agents,fitnessArr,POPULATION_SIZE):
        self.newGeneration = []
        self.POPULATION_SIZE = POPULATION_SIZE
        self.mutation_rate = math.exp(-t/GENERATION_COUNT) * abs(math.cos(t/2)) * MAX_MUTATION_RATE
        print("Current mutation rate:", self.mutation_rate)
        self.selection(agents,fitnessArr)
        self.crossover(agents)
        self.mutate()

    def selection(self,agents,fitnessArr):
        global best_score_count
        global STAGNATION
        if best_score_count < STAGNATION:
            print("Selecting the", SELECTION_SIZE, "best rockets for breeding")
            for i in range(len(fitnessArr)):
                self.newGeneration.append(agents[fitnessArr[i][0]])
            print("Adding", NEWBLOOD_SIZE, "brand new rockets to the breeding pool")
            for i in range(NEWBLOOD_SIZE):
                self.newGeneration.append(AI())
        else:
            print("Stagnation: kill all but the very best and bring in fresh blood")
            for i in range(PRESERVE_NB):
                self.newGeneration.append(agents[fitnessArr[i][0]])
            print("Adding", self.POPULATION_SIZE - PRESERVE_NB, "brand new rockets to the breeding pool")
            for i in range(self.POPULATION_SIZE - PRESERVE_NB):
                self.newGeneration.append(AI())

    def reproduce(self, parent1, parent2):
        newAI = AI()
        for i in range(CHROMOSOMES_LAYER_NB):
            for j in range(CHROMOSOMES_LAYER_WIDTH):
                if random.uniform(0,1) > 0.5:
                    newAI.weights[i][j] = parent1.weights[i][j]
                else:
                    newAI.weights[i][j] = parent2.weights[i][j]
        self.newGeneration.append(newAI)

    def crossover(self,agents):
        global best_score_count
        global STAGNATION
        if best_score_count < STAGNATION:
            pairs = list(combinations(self.newGeneration, 2))
            for z in range(round(len(pairs) / 2)):
                self.reproduce(pairs[z][0],pairs[z][1])
            print("Adding", self.POPULATION_SIZE - len(self.newGeneration), "brand new rockets to total population")
            for i in range(self.POPULATION_SIZE - len(self.newGeneration)):
                self.newGeneration.append(AI())
        else:
            best_score_count = 0

    def mutate(self):
        newgen_mutations = 0
        for i in range(PRESERVE_NB, len(self.newGeneration)):
            if random.uniform(0,1) <= self.mutation_rate:
                newgen_mutations += 1
                nb = random.randint(1,MAX_MUTATIONS)
                for j in range(nb):
                    layer = random.randint(0,CHROMOSOMES_LAYER_NB - 1)
                    idx = random.randint(0,CHROMOSOMES_LAYER_WIDTH - 1)
                    if layer == 0 :
                        nw1 = (self.newGeneration[i].weights[0][idx][0]+random.uniform(-1,1))/2
                        nw2 = (self.newGeneration[i].weights[0][idx][1]+random.uniform(-1,1))/2
                        self.newGeneration[i].weights[0][idx] = [nw1,nw2]
                    else:
                        nw = (self.newGeneration[i].weights[layer][idx]+random.uniform(-1,1))/2
                        self.newGeneration[i].weights[layer][idx] = nw
        print(newgen_mutations, "rockets have received random mutations")
class AI:
    def __init__(self,weights = False):
        self.output = False
        self.x = 0
        self.y = 0
        self.y_min = HEIGHT
        self.distance = HEIGHT
        self.v_final = 0
        self.rocket_mass = 0
        self.fuel_left = 0
        global current_id
        self.id = current_id
        current_id += 1
        self.transit_neurone_value = [None] * CHROMOSOMES_LAYER_WIDTH
        if weights :
            self.weights = weights
        else:
            self.weights = self.genWeights()

    def genWeights(self):
        arr = []
        tmp_arr = []
        for j in range(CHROMOSOMES_LAYER_WIDTH):
            tmp_arr.append([random.uniform(-1,1),random.uniform(-1,1)])
        arr.append(tmp_arr)
        for i in range(1, CHROMOSOMES_LAYER_NB):
            tmp_arr2 = []
            for j in range(CHROMOSOMES_LAYER_WIDTH):
                tmp_arr2.append(random.uniform(-1,1),)
            arr.append(tmp_arr2)
        return arr

    def getOutput(self,input1,input2):
        output = 0
        for i in range(CHROMOSOMES_LAYER_WIDTH):
            self.transit_neurone_value[i] = self.sigmoid(self.weights[0][i][0]*float(input1) +self.weights[0][i][1])*float(input2)
        for i in range(1, CHROMOSOMES_LAYER_NB-1):
            interm = np.sum(self.transit_neurone_value[i-1])
            for j in range(CHROMOSOMES_LAYER_WIDTH):
                self.transit_neurone_value[j] = self.sigmoid(interm * float(self.weights[i][j]))
        for i in range(CHROMOSOMES_LAYER_WIDTH):
            output += self.weights[-1][i] * self.transit_neurone_value[i]

        self.output = self.sigmoid(output) > 0.5
        return self.output

    def sigmoid(self,input):
        if input < 0:
            return 1 - 1/(1 + math.exp(input))
        else:
            return 1/(1 + math.exp(-input))

    def fitnessCalc(self):
        if self.y <= 0:
            if self.v_final >= V_MAX_TOUCHDOWN:
                return 1/self.v_final
            else:
                return self.fuel_left*1e-3
        else:
            if self.y_min == 0:
                return self.fuel_left*1e-5
            else:
                return 1 / self.y_min

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
        global best_score
        global last_best_score
        global best_score_count

        for i in range(len(self.agents)):
            self.fitnessArr.append((i,
                                    self.agents[i].fitnessCalc(),
                                    "id: " + str(self.agents[i].id),
                                    "vfinal: " + str(round(self.agents[i].v_final, 2)),
                                    "hfinal: " + str(round(self.agents[i].distance, 2)),
                                    "fleft: " + str(round(self.agents[i].fuel_left))))

        self.fitnessArr.sort(reverse=True, key = lambda x: x[1])

        genome = Genome(self.agents,self.fitnessArr[:SELECTION_SIZE], self.POPULATION_SIZE)

        if self.fitnessArr[0][1] == best_score and self.fitnessArr[PRESERVE_NB][1] == last_best_score:
            best_score_count += 1
            print("best scores", best_score, "and", last_best_score, "occured", best_score_count, "times")
        else:
            best_score = self.fitnessArr[0][1]
            last_best_score = self.fitnessArr[PRESERVE_NB - 1][1]
            best_score_count = 0
            print("resetting best score", best_score)

        print(DISPLAY_SCORES, "best scores:")
        for i in range(DISPLAY_SCORES):
            print(self.fitnessArr[i])

        if not signal:
            self.agents = genome.newGeneration
        else:
            best = self.agents[self.fitnessArr[-1][0]]
            self.agents = []
            for i in range(self.POPULATION_SIZE):
                self.agents.append(best)
            print(best.v_final,"m/s vitesse finale")
            print(best.distance,"m altitude finale")

        self.fitnessArr = []