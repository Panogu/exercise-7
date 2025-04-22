import math
import tsplib95
import networkx as nx

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
"""
class Environment:
    def __init__(self, rho, ant_population = 48):

        self.rho = rho
        self.ant_population = ant_population  # Number of ants in the colony
        
        # Initialize the environment topology
        self.tsp = tsplib95.load('att48-specs/att48.tsp')

        self.graph = self.tsp.get_graph()

        # Remove all edges which lead from a node to itself (initial weight == 0)
        for i, j in self.graph.edges():
            if self.graph[i][j]["weight"] == 0:
                self.graph.remove_edge(i, j)


        # Add the distance to the edges by taking the coordinates and calculating the distance
        distances = {}
        for i, j in self.graph.edges():
            x1, y1 = self.tsp.node_coords[i]
            x2, y2 = self.tsp.node_coords[j]
            
            # The distance is recalculated as the pseudo-euclidean distance
            xd = x1 - x2
            yd = y1 - y2
            rij = math.sqrt((xd * xd + yd * yd) / 10.0)
            tij = round(rij)
            if tij < rij:
                dij = tij + 1
            else:
                dij = tij
            
            distances[(i, j)] = dij

        nx.set_edge_attributes(self.graph, distances, 'weight')

        # Initialize the pheromone map in the environment
        self.initialize_pheromone_map()

    # Initialize the pheromone trails in the environment
    def initialize_pheromone_map(self, n_cities = 48):
        # Load the initial optimal solution from the opt.tour file
        opt = tsplib95.load('att48-specs/att48.opt.tour')

        # Get the tour from the optimal solution
        tour = opt.tours[0]

        # Use the nodes to calculate the cost of the optimal solution using the graph
        cost = 0
        for i in range(len(tour) - 1):
            cost += self.graph[tour[i]][tour[i + 1]]['weight']
        
        pheromones = {}
        for i, j in self.graph.edges():
            # From the book: Experimentally, a good value for x was found to be c, while a good value for t0 was found to be 1/(n*C_nn), where n is the number of cities in the TSP instance and C nn is the length of a nearest-neighbor tour.
            # FOR EACH ANT --> Thus * self.ant_population
            pheromones[(i, j)] = self.ant_population / (n_cities * cost)

        nx.set_edge_attributes(self.graph, pheromones, 'pheromones')

    # Update the pheromone trails in the environment
    def update_pheromone_map(self, update_map):

        # Using two loops to adhere to the task description (first evaporate, then deposit), this could be made more efficient

        # Evaporate pheromone trails
        for i, j in self.graph.edges():
            pheromones = self.graph[i][j]['pheromones']
            pheromones *= (1 - self.rho)
            self.graph[i][j]['pheromones'] = pheromones

        # Add pheromone to the pheromone map based on the ants' paths
        for i, j in update_map.keys():
            pheromones = self.graph[i][j]['pheromones']
            pheromones += update_map[(i, j)]
            self.graph[i][j]['pheromones'] = pheromones

    # Get the pheromone trails in the environment
    def get_pheromone_map(self):
        return nx.get_edge_attributes(self.graph, 'pheromones')
    
    def get_pheromones(self, i, j):
        return self.graph.edges[(i, j)]["pheromones"]
    
    # Get the environment topology
    def get_possible_locations(self):
        return list(self.graph.nodes())
    
    # Get the weight as distance
    def get_distance(self, i, j):
        return self.graph.edges[(i, j)]["weight"]

    
