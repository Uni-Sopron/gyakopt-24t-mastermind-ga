import random
import string
import matplotlib.pyplot as plt

CHARACTERS = string.ascii_letters + string.digits + string.punctuation

def generate_random_string(length):
    return ''.join(random.choice(CHARACTERS) for _ in range(length))

def fitness_function(candidate, target):
    return sum(1 for a, b in zip(candidate, target) if a == b)

def select_parents(population, fitness_scores, num_parents):
    parents = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)[:num_parents]
    return [p[0] for p in parents]

def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    return parent1[:crossover_point] + parent2[crossover_point:]

def mutate(candidate, mutation_rate):
    candidate_list = list(candidate)
    for i in range(len(candidate_list)):
        if random.random() < mutation_rate:
            candidate_list[i] = random.choice(CHARACTERS)
    return ''.join(candidate_list)

def genetic_algorithm(test_string, population_size, iterations, elitism, crossover_num, generation, mutation_rate):
    population = [generate_random_string(len(test_string)) for _ in range(population_size)]
    
    for i in range(iterations):
        fitness_scores = [fitness_function(individual, test_string) for individual in population]
        next_population = select_parents(population, fitness_scores, elitism)

        non_generated_population_size = population_size - generation
        
        while len(next_population) < non_generated_population_size:
            parents = random.sample(next_population[:elitism], 2)
            for _ in range(crossover_num):
                offspring = crossover(parents[0], parents[1])
                offspring = mutate(offspring, mutation_rate)
                next_population.append(offspring)
        
        next_population = next_population[:non_generated_population_size] + [generate_random_string(len(test_string)) for _ in range(generation)]
        population = next_population
        current_best_solution = max(population, key=lambda x: fitness_function(x, test_string))
        if fitness_function(current_best_solution, test_string) == len(test_string):
            print("Perfect solution found in " + str(i) + ". iteration")
            return current_best_solution

    best_solution = max(population, key=lambda x: fitness_function(x, test_string))
    return best_solution

def generate_plot(results, param_for_graph):
    param_values = [result[param_for_graph] for result in results]
    fitness_scores = [result["fitness_score"] for result in results]
    
    # Assuming only one param is different at a time between populations
    if param_for_graph == "string_length":
        fitness_scores = [score / length for score, length in zip(fitness_scores, param_values)]
        plt.ylabel('Fitness Score / String Length')
    else:
        plt.ylabel('Fitness Score')

    plt.plot(param_values, fitness_scores, marker='o')
    plt.xlabel(param_for_graph)
    plt.title('Genetic Algorithm Performance')
    plt.grid(True)
    plt.show()

# Decide, if you want to test on a single string or a set of parametrized cases
use_single_string = True
# TRY OUT HERE!

if use_single_string:
    string_length = 100
    test_string = generate_random_string(string_length)
    print("Test string is: " + test_string)
    population_size = 600
    iterations = 300
    elitism = 20
    crossover_num = 2
    generation = 10
    mutation_rate = 0.01
    best_solution = genetic_algorithm(test_string, population_size, iterations, elitism, crossover_num, generation, mutation_rate)
    print("Best solution:", best_solution)
    print("Fitness score:", fitness_function(best_solution, test_string))
else:
    # Use a parameter of the following to create a graph: 
    # stringLength populationSize iterations elitism crossoverNum generation mutationRate
    param_for_graph = "population_size"
    parameter_sets = [
        {"string_length": 100, "population_size": 100, "iterations": 100, "elitism": 20, "crossover_num": 2, "generation": 10, "mutation_rate": 0.01},
        {"string_length": 100, "population_size": 200, "iterations": 100, "elitism": 20, "crossover_num": 2, "generation": 10, "mutation_rate": 0.01},
        {"string_length": 100, "population_size": 300, "iterations": 100, "elitism": 20, "crossover_num": 2, "generation": 10, "mutation_rate": 0.01},
        {"string_length": 100, "population_size": 400, "iterations": 100, "elitism": 20, "crossover_num": 2, "generation": 10, "mutation_rate": 0.01},
        {"string_length": 100, "population_size": 500, "iterations": 100, "elitism": 20, "crossover_num": 2, "generation": 10, "mutation_rate": 0.01},
    ]

    results = []

    for params in parameter_sets:
        string_length = params["string_length"]
        test_string = generate_random_string(string_length)
        population_size = params["population_size"]
        iterations = params["iterations"]
        elitism = params["elitism"]
        crossover_num = params["crossover_num"]
        generation = params["generation"]
        mutation_rate = params["mutation_rate"]

        best_solution = genetic_algorithm(test_string, population_size, iterations, elitism, crossover_num, generation, mutation_rate)
        fitness_score = fitness_function(best_solution, test_string)
        
        results.append({param_for_graph: params[param_for_graph], "fitness_score": fitness_score})
    generate_plot(results, param_for_graph)
