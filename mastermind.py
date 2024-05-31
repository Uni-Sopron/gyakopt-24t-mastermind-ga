import random
import string
import matplotlib.pyplot as plt
from dataclasses import dataclass
import argparse
import json

CHARACTERS = string.ascii_letters + string.digits + string.punctuation

def load_config_from_json(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return GAConfig(**data)

@dataclass
class GAConfig:
    population_size: int
    iterations: int
    elitism: int
    crossover_num: int
    random_generated_candidate_num: int
    mutation_rate: float

def generate_random_string(length):
    return ''.join(random.choice(CHARACTERS) for _ in range(length))

def fitness_function(candidate, target):
    return sum(1 for a, b in zip(candidate, target) if a == b)

def select_parents(population, num_parents, test_string):
    fitness_scores = [fitness_function(individual, test_string) for individual in population]
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

def genetic_algorithm(test_string, config):
    population = [generate_random_string(len(test_string)) for _ in range(config.population_size)]
    for i in range(config.iterations):
        best_candidates = select_parents(population, config.elitism, test_string)

        next_population = best_candidates[:]
        generated_candidates = [generate_random_string(len(test_string)) for _ in range(config.random_generated_candidate_num)]
        next_population.extend(generated_candidates)
        
        while len(next_population) < config.population_size:
            parents = random.sample(best_candidates, 2)
            for _ in range(config.crossover_num):
                if len(next_population) < config.population_size:
                    offspring = crossover(parents[0], parents[1])
                    offspring = mutate(offspring, config.mutation_rate)
                    next_population.append(offspring)
        
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

def dict_to_gaconfig(config_dict):
    config_dict_copy = config_dict.copy()
    config_dict_copy.pop('string_length', None)
    return GAConfig(**config_dict_copy)

def main(use_single_string):
    if use_single_string:
        string_length = 100
        test_string = generate_random_string(string_length)
        print("Test string is: " + test_string)
        config = load_config_from_json('single_string_config.json')
        best_solution = genetic_algorithm(test_string, config)
        print("Best solution:", best_solution)
        print("Fitness score:", fitness_function(best_solution, test_string))
    else:
        # Use a parameter of the following to create a graph: 
        # string_length population_size iterations elitism crossover_num random_generated_candidate_num mutation_rate
        param_for_graph = "population_size"
        parameter_sets = [
            {"string_length": 100, "population_size": 100, "iterations": 100, "elitism": 20, "crossover_num": 2, "random_generated_candidate_num": 10, "mutation_rate": 0.01},
            {"string_length": 100, "population_size": 200, "iterations": 100, "elitism": 20, "crossover_num": 2, "random_generated_candidate_num": 10, "mutation_rate": 0.01},
            {"string_length": 100, "population_size": 300, "iterations": 100, "elitism": 20, "crossover_num": 2, "random_generated_candidate_num": 10, "mutation_rate": 0.01},
            {"string_length": 100, "population_size": 400, "iterations": 100, "elitism": 20, "crossover_num": 2, "random_generated_candidate_num": 10, "mutation_rate": 0.01},
            {"string_length": 100, "population_size": 500, "iterations": 100, "elitism": 20, "crossover_num": 2, "random_generated_candidate_num": 10, "mutation_rate": 0.01},
        ]

        results = []

        for params in parameter_sets:
            string_length = params["string_length"]
            test_string = generate_random_string(string_length)
            config = dict_to_gaconfig(params)

            best_solution = genetic_algorithm(test_string, config)
            fitness_score = fitness_function(best_solution, test_string)
            
            results.append({param_for_graph: params[param_for_graph], "fitness_score": fitness_score})
        generate_plot(results, param_for_graph)


parser = argparse.ArgumentParser(description='Use single string?')
parser.add_argument('--single', action='store_true')
args = parser.parse_args()
main(use_single_string=args.single)