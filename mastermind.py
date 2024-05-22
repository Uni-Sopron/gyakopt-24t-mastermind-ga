import random
import string
import matplotlib.pyplot as plt

def generateRandomString(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    randomString = ''.join(random.choice(characters) for _ in range(length))
    return randomString

def fitnessFunction(candidate, target):
    return sum(1 for a, b in zip(candidate, target) if a == b)

def selectParents(population, fitnessScores, numParents):
    parents = sorted(zip(population, fitnessScores), key=lambda x: x[1], reverse=True)[:numParents]
    return [p[0] for p in parents]

def crossover(parent1, parent2):
    crossoverPoint = random.randint(0, len(parent1) - 1)
    return parent1[:crossoverPoint] + parent2[crossoverPoint:]

def mutate(candidate, mutationRate):
    characters = string.ascii_letters + string.digits + string.punctuation
    candidateList = list(candidate)
    for i in range(len(candidateList)):
        if random.random() < mutationRate:
            candidateList[i] = random.choice(characters)
    return ''.join(candidateList)

def geneticAlgorithm(testString, populationSize, iterations, elitism, crossoverNum, generation, mutationRate):
    population = [generateRandomString(len(testString)) for _ in range(populationSize)]
    
    for i in range(iterations):
        fitnessScores = [fitnessFunction(individual, testString) for individual in population]
        nextPopulation = selectParents(population, fitnessScores, elitism)

        nonGeneratedPopulationSize = populationSize - generation
        
        while len(nextPopulation) < nonGeneratedPopulationSize:
            parents = random.sample(nextPopulation[:elitism], 2)
            for _ in range(crossoverNum):
                offspring = crossover(parents[0], parents[1])
                offspring = mutate(offspring, mutationRate)
                nextPopulation.append(offspring)
        
        nextPopulation = nextPopulation[:nonGeneratedPopulationSize] + [generateRandomString(len(testString)) for _ in range(generation)]
        population = nextPopulation
        currentBestSolution = max(population, key=lambda x: fitnessFunction(x, testString))
        if(fitnessFunction(currentBestSolution, testString)==len(testString)):
            print("Perfect solution found in "+str(i)+". iteration")
            return currentBestSolution

    bestSolution = max(population, key=lambda x: fitnessFunction(x, testString))
    return bestSolution

def generatePlot(results, paramForGraph):
    paramValues = [result[paramForGraph] for result in results]
    fitnessScores = [result["fitnessScore"] for result in results]
    
    # Assuming only one param is different at a time between populations
    if paramForGraph == "stringLength":
        fitnessScores = [score / length for score, length in zip(fitnessScores, paramValues)]
        plt.ylabel('Fitness Score / String Length')
    else:
        plt.ylabel('Fitness Score')

    plt.plot(paramValues, fitnessScores, marker='o')
    plt.xlabel(paramForGraph)
    plt.title('Genetic Algorithm Performance')
    plt.grid(True)
    plt.show()

# Decide, if you want to test on a single string or a set of parametrized cases
useSingleString = True

# TRY OUT HERE!
if(useSingleString):
    stringLength = 100
    testString = generateRandomString(stringLength)
    print("Test string is: "+testString)
    populationSize = 600
    iterations = 300
    elitism = 20
    crossoverNum = 2
    generation = 10
    mutationRate = 0.01
    bestSolution = geneticAlgorithm(testString, populationSize, iterations, elitism, crossoverNum, generation, mutationRate)
    print("Best solution:", bestSolution)
    print("Fitness score:", fitnessFunction(bestSolution, testString))
else:

    # Use a parameter of the following to create a graph: 
    # stringLength populationSize iterations elitism crossoverNum generation mutationRate
    paramForGraph = "populationSize"
    parameterSets = [
        {"stringLength": 100, "populationSize": 100, "iterations": 100, "elitism": 20, "crossoverNum": 2, "generation": 10, "mutationRate": 0.01},
        {"stringLength": 100, "populationSize": 100, "iterations": 100, "elitism": 20, "crossoverNum": 2, "generation": 10, "mutationRate": 0.01},
        {"stringLength": 100, "populationSize": 100, "iterations": 100, "elitism": 20, "crossoverNum": 2, "generation": 10, "mutationRate": 0.01},
        {"stringLength": 100, "populationSize": 100, "iterations": 100, "elitism": 20, "crossoverNum": 2, "generation": 10, "mutationRate": 0.01},
        {"stringLength": 100, "populationSize": 100, "iterations": 100, "elitism": 20, "crossoverNum": 2, "generation": 10, "mutationRate": 0.01},
    ]

    results = []

    for params in parameterSets:
        stringLength = params["stringLength"]
        testString = generateRandomString(stringLength)
        populationSize = params["populationSize"]
        iterations = params["iterations"]

        elitism = params["elitism"]
        crossoverNum = params["crossoverNum"]
        generation = params["generation"]
        mutationRate = params["mutationRate"]

        bestSolution = geneticAlgorithm(testString, populationSize, iterations, elitism, crossoverNum, generation, mutationRate)
        fitnessScore = fitnessFunction(bestSolution, testString)
        
        results.append({paramForGraph: params[paramForGraph], "fitnessScore": fitnessScore})
    generatePlot(results, paramForGraph)






