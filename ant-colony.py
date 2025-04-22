import numpy as np

from environment import Environment
from ant import Ant 

import random

# Class representing the ant colony
"""
    ant_population: the number of ants in the ant colony
    iterations: the number of iterations 
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
    rho: pheromone evaporation rate
"""
class AntColony:
    def __init__(self, ant_population: int, iterations: int, alpha: float, beta: float, rho: float):
        self.ant_population = ant_population
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho 

        # Initialize the environment of the ant colony
        self.environment = Environment(self.rho)

        # Initilize the list of ants of the ant colony
        self.ants = []

        # Initialize the ants of the ant colony
        for i in range(ant_population):
            
            # Initialize an ant on a random initial location 
            ant = Ant(self.alpha, self.beta, random.randrange(1, 49))

            # Position the ant in the environment of the ant colony so that it can move around
            ant.join(self.environment)
        
            # Add the ant to the ant colony
            self.ants.append(ant)

    # Solve the ant colony optimization problem  
    def solve(self):
        # The solution will be a list of the visited cities
        solution = []

        # Initially, the shortest distance is set to infinite
        shortest_distance = np.inf

        for i in range(self.iterations):
            
            # Loop through every ant
            for ant in self.ants:
                visited_locations = ant.run()
                
                # Check if this ant found a better solution
                if ant.traveled_distance < shortest_distance:
                    shortest_distance = ant.traveled_distance
                    solution = visited_locations.copy()  # Make a copy to avoid reference issues

            # Aggregate the pheromone values for the edges visited by the ants
            pheromones_to_deposit = {}
            for ant in self.ants:
                # Get all pheromones to deposit
                ant_pheromones = ant.get_pheromones_to_deposit()

                for key in ant_pheromones.keys():
                    if key in pheromones_to_deposit:
                        pheromones_to_deposit[key] += ant_pheromones[key]
                    else:
                        pheromones_to_deposit[key] = ant_pheromones[key]

            # Update the pheromone values in the environment
            self.environment.update_pheromone_map(pheromones_to_deposit)

            # Print the iteration and current best distance
            # print(f"Iteration: {i + 1}/{self.iterations}, Current best distance: {shortest_distance}")

        return solution, shortest_distance


def main():

    random.seed(69)  # Set a random seed for reproducibility

    # Utilize different parameters for the ant colony optimization algorithm (some are pretty extreme)
    ant_population_pool = [48]
    iterations_pool = [1, 15, 35, 60]
    alpha_pool = [0.75, 1, 1.5]
    beta_pool = [1, 2, 2.5, 3]
    rho_pool = [0.3, 0.5, 0.8]

    # Loop through the different parameters and print the results
    results_dict = {}
    for ant_population in ant_population_pool:
        for iterations in iterations_pool:
            for alpha in alpha_pool:
                for beta in beta_pool:
                    for rho in rho_pool:
                        print(f"Ant Population: {ant_population}, Iterations: {iterations}, Alpha: {alpha}, Beta: {beta}, Rho: {rho}")

                        # Initialize the ant colony with the current parameters
                        ant_colony = AntColony(ant_population, iterations, alpha, beta, rho)

                        # Solve the ant colony optimization problem
                        solution, distance = ant_colony.solve()
                        #print("Solution: ", solution)
                        print("Solution found with distance: ", distance)

                        # Store parameters and results in a dictionary
                        results_dict[(ant_population, iterations, alpha, beta, rho)] = {
                            'solution': solution,
                            'distance': distance
                        }

    # Find the best solution and parameters
    best_solution_and_parameters = min(results_dict.items(), key=lambda x: x[1]['distance'])[1]

    print("Best solution found with distance: ", best_solution_and_parameters['distance'])
    print("Best parameters: ", [k for k, v in results_dict.items() if v == best_solution_and_parameters][0])

    # Save the results to a file
    with open("results.txt", "w") as f:
        for params, result in results_dict.items():
            f.write(f"Parameters: {params}, Solution: {result['solution']}, Distance: {result['distance']}\n")

if __name__ == '__main__':
    main()    