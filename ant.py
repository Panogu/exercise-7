import math
import random
import numpy as np

# Class representing an artificial ant of the ant colony
"""
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
"""
class Ant():
    def __init__(self, alpha: float, beta: float, initial_location):
        self.alpha = alpha
        self.beta = beta
        self.initial_location = initial_location
        self.traveled_distance = 0
        self.visited_locations = []

    # The ant runs to visit all the possible locations of the environment 
    def run(self):
        self.current_location = self.initial_location
        self.visited_locations = [self.current_location]  # Start with the initial location
        self.traveled_distance = 0
        self.open_locations = self.environment.get_possible_locations()
        self.open_locations.remove(self.current_location)

        # While there are still locations to visit
        while len(self.open_locations) > 0:
            # Select the next path
            next_location = self.select_path()
            
            # Calculate distance to next location
            self.traveled_distance += self.environment.get_distance(self.current_location, next_location)
            
            # Update current location
            self.current_location = next_location
            self.visited_locations.append(next_location)

            # Remove the visited location from the list of open locations
            self.open_locations.remove(next_location)

        # Add the return to the initial location to complete the tour
        self.traveled_distance += self.environment.get_distance(self.current_location, self.initial_location)
        self.visited_locations.append(self.initial_location)  # Complete the cycle by returning to start
        
        return self.visited_locations

    # Select the next path based on the random proportional rule of the ACO algorithm
    def select_path(self):
        # ACO algorithm
        # Calculate the possibility for selecting the specific next path

        # Sum up the weights to all next locations
        sum_weights = 0
        for possible_next_location in self.open_locations:
            # Note: we use 1/distance because shorter distances should have higher probability
            distance_factor = 1.0 / self.get_distance(possible_next_location) if self.get_distance(possible_next_location) > 0 else 1.0
            sum_weights += (self.get_pheromones(possible_next_location) ** self.alpha * distance_factor ** self.beta)

        possibilities = {}
        for possible_next_location in self.open_locations:
            distance_factor = 1.0 / self.get_distance(possible_next_location) if self.get_distance(possible_next_location) > 0 else 1.0
            possibilities[possible_next_location] = (self.get_pheromones(possible_next_location) ** self.alpha * distance_factor ** self.beta)/(sum_weights)

        # Randomly select a next location based on the above possibilities
        return np.random.choice(list(possibilities.keys()), 1, p=list(possibilities.values()))[0]

    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment
    
    def get_distance(self, target_location):
        # As the pseudo euclidean distance is static for the existing nodes, it can be extracted from the environment where it is also calculated initially
        return self.environment.get_distance(self.current_location, target_location)
    
    def get_pheromones(self, target_location):
        return self.environment.get_pheromones(self.current_location, target_location)
    
    def get_pheromones_to_deposit(self):
        pheromones_to_deposit = {}
        
        # Add pheromones for all visited edges (now includes return to start)
        for i in range(len(self.visited_locations) - 1):
            from_loc = self.visited_locations[i]
            to_loc = self.visited_locations[i + 1]
            pheromones_to_deposit[(from_loc, to_loc)] = 1.0 / self.traveled_distance
        
        return pheromones_to_deposit

