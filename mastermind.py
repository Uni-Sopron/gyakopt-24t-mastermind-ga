import random
import string
import matplotlib.pyplot as plt
from dataclasses import dataclass
import argparse
import json
import os

CHARACTERS = string.ascii_letters + string.digits + string.punctuation

def load_config_from_json(filepath):
    """
    Load GAConfig from a JSON file.

    Args:
        filepath (str): The path to the JSON file containing the configuration.

    Returns:
        GAConfig: The GAConfig object with the loaded configuration.
    """
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
    """
    Generate a random string of a given length.

    Args:
        length (int): The length of the string to generate.

    Returns:
        str: The generated random string.
    """
    return ''.join(random.choice(CHARACTERS) for _ in range(length))

def fitness_function(candidate, target):
    """
    Calculate the fitness score of a candidate string compared to the target string.

    Args:
        candidate (str): The candidate string.
        target (str): The target string.

    Returns:
        int: The fitness score indicating the number of matching characters.
    """
    return sum(1 for a, b in zip(candidate, target) if a == b)

def select_parents(population, num_parents, test_string):
    """
    Select the top candidates (parents) from the population based on fitness scores.

    Args:
        population (list of str): The population of candidate strings.
        num_parents (int): The number of parents to select.
        test_string (str): The target string.

    Returns:
        list of str: The selected parent strings.
    """
    fitness_scores = [fitness_function(individual, test_string) for individual in population]
    parents = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)[:num_parents]
    return [p[0] for p in parents]

def crossover(parent1, parent2):
    """
    Perform a crossover between two parent strings to create an offspring.

    Args:
        parent1 (str): The first parent string.
        parent2 (str): The second parent string.

    Returns:
        str: The offspring string resulting from the crossover.
    """
    crossover_point = random.randint(0, len(parent1) - 1)
    return parent1[:crossover_point] + parent2[crossover_point:]

def mutate(candidate, mutation_rate):
    """
    Mutate a candidate string based on the mutation rate.

    Args:
        candidate (str): The candidate string.
        mutation_rate (float): The mutation rate.

    Returns:
        str: The mutated candidate string.
    """
    candidate_list = list(candidate)
    for i in range(len(candidate_list)):
        if random.random() < mutation_rate:
            candidate_list[i] = random.choice(CHARACTERS)
    return ''.join(candidate_list)

def log_results(filepath, config, test_string, best_solution, fitness_score):
    """
    Log the GAConfig settings, test string, best solution, and its fitness score to a file.

    Args:
        filepath (str): The path to the log file.
        config (GAConfig): The configuration for the genetic algorithm.
        test_string (str): The target string.
        best_solution (str): The best solution found by the genetic algorithm.
        fitness_score (int): The fitness score of the best solution.
    """
    with open(filepath, 'a') as file:
        file.write(f"GAConfig: {config}\n")
        file.write(f"Test string: {test_string}\n")
        file.write(f"Best solution: {best_solution}\n")
        file.write(f"Fitness score: {fitness_score}\n\n")

def genetic_algorithm(test_string, config, log_filepath):
    """
    Run the genetic algorithm to find the best solution for the target string.

    Args:
        test_string (str): The target string.
        config (GAConfig): The configuration for the genetic algorithm.
        log_filepath (str): The path to the log file.

    Returns:
        str: The best solution found by the genetic algorithm.
    """
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
            log_results(log_filepath, config, test_string, current_best_solution, len(test_string))
            return current_best_solution

    best_solution = max(population, key=lambda x: fitness_function(x, test_string))
    fitness_score = fitness_function(best_solution, test_string)
    log_results(log_filepath, config, test_string, best_solution, fitness_score)
    return best_solution

def generate_plot(results, param_for_graph):
    """
    Generate and display a plot of the genetic algorithm performance.

    Args:
        results (list of dict): The results containing parameter values and fitness scores.
        param_for_graph (str): The parameter to be plotted on the x-axis.
    """
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
    """
    Convert a dictionary to a GAConfig object, excluding the 'string_length' key if present.

    Args:
        config_dict (dict): The dictionary containing configuration parameters.

    Returns:
        GAConfig: The GAConfig object created from the dictionary.
    """
    config_dict_copy = config_dict.copy()
    config_dict_copy.pop('string_length', None)
    return GAConfig(**config_dict_copy)

def main(use_single_string):
    """
    Main function to run the genetic algorithm or generate a performance plot.

    Args:
        use_single_string (bool): Flag to indicate if a single string configuration should be used.
    """
    log_filepath = 'log.txt'
    if os.path.exists(log_filepath):
        os.remove(log_filepath)

    if use_single_string:
        string_length = 100
        test_string = generate_random_string(string_length)
        print("Test string is: " + test_string)
        config = load_config_from_json('single_string_config.json')
        best_solution = genetic_algorithm(test_string, config, log_filepath)
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

            best_solution = genetic_algorithm(test_string, config, log_filepath)
            fitness_score = fitness_function(best_solution, test_string)
            
            results.append({param_for_graph: params[param_for_graph], "fitness_score": fitness_score})
        generate_plot(results, param_for_graph)


parser = argparse.ArgumentParser(description='Use single string?')
parser.add_argument('--single', action='store_true')
args = parser.parse_args()
main(use_single_string=args.single)
