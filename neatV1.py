import random 
import math

SELECTION_SIZE = 50
DISPLAY_SCORES = 5
# CH nb must be par
CHROMOSOMES_LAYER_WIDTH = 32
CHROMOSOMES_LAYER_NB = 2
MAX_MUTATIONS = 20
MUTATION_RATE = 0.3 # ratio

def genWeights():
    arr1 = []
    arr2 = []
    for i in range(CHROMOSOMES_LAYER_WIDTH):
        arr1.append([random.uniform(-1,1),random.uniform(-1,1)])
        arr2.append(random.uniform(-1,1),)
    return [arr1, arr2]

class Genome:
    def __init__(self,agents,fitnessArr,POPULATION_SIZE):
        self.newGeneration = []
        self.defects = []
        self.POPULATION_SIZE = POPULATION_SIZE
        self.selection(agents,fitnessArr)
        self.crossover(agents)
        self.mutate(False)

    def selection(self,agents,fitnessArr):
        for i in range(len(fitnessArr)):
            self.defects.append(fitnessArr[i][1] == 0)
            self.newGeneration.append(agents[fitnessArr[i][0]])

    def crossover(self,agents):
        cut = random.randint(0,SELECTION_SIZE - 1)
        sel1 = random.randint(0,cut)
        sel2 = random.randint(cut,SELECTION_SIZE - 1)
        for z in range(cut):
            if z < sel1:
                parent1 = self.newGeneration[z]
                parent2 = self.newGeneration[z+1]
                defect = self.defects[z] or self.defects[z + 1]
                newAI = AI()
                for i in range(CHROMOSOMES_LAYER_NB):
                    for j in range(CHROMOSOMES_LAYER_WIDTH):
                        if random.uniform(0,1) > 0.5:
                            newAI.weights[i][j] = parent1.weights[i][j]
                        else:
                            newAI.weights[i][j] = parent2.weights[i][j]
                self.newGeneration.append(newAI)
                self.mutate(defect)
        for z in range(cut,len(self.newGeneration) - 1):
            if z < sel2:
                parent1 = self.newGeneration[z]
                parent2 = self.newGeneration[z+1]
                defect = self.defects[z] or self.defects[z + 1]
                newAI = AI()
                for i in range(CHROMOSOMES_LAYER_NB):
                    for j in range(CHROMOSOMES_LAYER_WIDTH):
                        if random.uniform(0,1) > 0.5:
                            newAI.weights[i][j] = parent1.weights[i][j]
                        else:
                            newAI.weights[i][j] = parent2.weights[i][j]
                self.newGeneration.append(newAI)
                self.mutate(defect)
        ran = random.choices(agents, k=(self.POPULATION_SIZE - len(self.newGeneration)))
        self.newGeneration.extend(ran)

    def mutate(self, is_defect):
        if is_defect:
            print("mutate: we have a defect")
            self.newGeneration[-1].weights = genWeights()
        else:
            if random.uniform(0,1) <= MUTATION_RATE:
                nb = random.randint(1,MAX_MUTATIONS)
                print("mutate: random mutation,", nb, "chromosomes")
                for i in range(nb):
                    layer = random.randint(0,1)
                    if layer == 0 :
                        self.newGeneration[-1].weights[0][random.randint(0,1)] = [random.uniform(-1,1),random.uniform(-1,1)]
                    else:
                        self.newGeneration[-1].weights[1][random.randint(0,1)] = random.uniform(-1,1)
class AI:
    def __init__(self,weights = False):
        self.output = False
        self.x = 0
        self.y = 0
        self.v_final = 0
        self.rocket_mass = 0
        if weights :
            self.weights = weights
        else:
            self.weights = genWeights()

    def getOutput(self,input1,input2):
        transit_neurone_value = []
        output = 0
        for i in range(CHROMOSOMES_LAYER_WIDTH):
            transit_neurone_value.append(self.sigmoid(self.weights[0][i][0]*float(input1) +self.weights[0][i][1])*float(input2))
        for i in range(CHROMOSOMES_LAYER_WIDTH):
            output += (float(self.weights[1][i]) * float(transit_neurone_value[i]))

        self.output = self.sigmoid(output) > 0.5
        return (self.sigmoid(output) > 0.5)

    def sigmoid(self,input):
        if input < 0:
            return 1 - 1/(1 + math.exp(input))
        else:
            return 1/(1 + math.exp(-input))

    def fitnessCalc(self):
        if self.y == 0:
            if self.v_final > 0.5:
                return 1/self.v_final
            else:
                return 1/self.v_final + self.fuel_left*1e-5
        else:
            return 0

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
        for i in range(len(self.agents)):
            self.fitnessArr.append((i,self.agents[i].fitnessCalc(),
                                    "vfinal: " + str(round(self.agents[i].v_final, 2)),
                                    "hfinal: " + str(round(self.agents[i].distance, 2)),
                                    "fleft: " + str(round(self.agents[i].fuel_left))))

        self.fitnessArr.sort(key = lambda x: x[1])

        genome = Genome(self.agents,self.fitnessArr[-SELECTION_SIZE:], self.POPULATION_SIZE)

        print("Five best scores : ", self.fitnessArr[-DISPLAY_SCORES:])

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