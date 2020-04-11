import random
import sys
import numpy as np
import time

################################################################################################
# Load Command Line Arguments and Data
################################################################################################

input_file_name = sys.argv[1]  # inputfilename.txt
output_file_name = sys.argv[2]  # outputfilename.txt
timeout = int(sys.argv[3])  # a rational number greater than 0

coordinates = np.loadtxt(input_file_name)  # loads data into coordinates

# example: $ python3.7 tsp-3510.py mat-test.txt output.txt 5

################################################################################################
# Compute Euclidean Distance Between All Points
################################################################################################

x_coordinates = coordinates[:,1]  # x coordinates
y_coordinates = coordinates[:,2]  # y coordinates
length = x_coordinates.shape[0]  # number of coordinates
x_tiled = np.tile(x_coordinates, (length, 1))  # copy the top row for all rows
y_tiled = np.tile(y_coordinates, (length, 1))  # copy the top row for all rows
x_diff = x_tiled - x_tiled.T  # subtract every possible x coordinate from one another
y_diff = y_tiled - y_tiled.T  # subtract every possible y coordinate from one another
euclidean_distance = np.rint(np.sqrt(np.square(x_diff) + np.square(y_diff)))  # euclidean distance formula rounded to int

#print(euclidean_distance[6][1])  # gets the euclidean distance between point 4 and 2

################################################################################################
# Genetic Algorithm Parameters
################################################################################################

population_size = 100  # number of routes in each population iteration
individual_mutation_rate = 0.2  # proportion of cities that are randomly changed in a route mutation
population_mutation_rate = 0.3  # proportion of routes that mutate each iteration
elite_size = 80  # size of population guaranteed to survive each iteration
survival_rate = 0  # rate of survival for not elite population each iteration


################################################################################################
# Genetic Algorithm Functions
################################################################################################

def generate_route():
    return random.sample(range(len(coordinates)), len(coordinates))


def get_route_length(route):
    route_length = 0
    for i in range(len(route)):
        route_length += euclidean_distance[route[i]][route[(i + 1) % len(route)]]
    return route_length


def create_population():
    return [(r, get_route_length(r)) for r in [generate_route() for i in range(population_size)]]


def sort_by_fitness(population):
    return sorted(population, key=lambda r: r[1])


def breed(route_1, route_2):
    a = int(random.random() * len(route_1[0]))
    b = int(random.random() * len(route_1[0]))
    part1 = route_1[0][min(a, b): max(a, b)]
    part2 = [city for city in route_2[0] if city not in part1]
    child = part1 + part2
    return child, get_route_length(child)


def breed_population(mating_pool, offspring_quantity):
    children = []
    for i in range(offspring_quantity):
        a = int(random.random() * len(mating_pool))
        b = int(random.random() * len(mating_pool))
        children.append(breed(mating_pool[a], mating_pool[b]))
    return children


def mutate_individual(route):
    for i in range(len(route[0])):
        if random.random() < individual_mutation_rate:
            victim = int(random.random() * len(route[0]))
            storage = route[0][victim]
            route[0][victim] = route[0][i]
            route[0][i] = storage
    return route[0], get_route_length(route[0])


def mutate_population(population):
    for i in range(len(population)):
        if random.random() < population_mutation_rate:
            population[i] = mutate_individual(population[i])
    return population


def select_pool(sorted_population):
    pool = sorted_population[0: elite_size]
    for i in range(elite_size, len(sorted_population)):
        if random.random() < survival_rate:
            pool.append(sorted_population[i])
    return pool


def create_new_generation(population):
    ranked_population = sort_by_fitness(population)
    mating_pool = select_pool(ranked_population)
    children = breed_population(mating_pool, population_size - len(mating_pool))
    children = mutate_population(children)
    return mating_pool + children


################################################################################################
# Output data to file
################################################################################################

def write_output(path):
    my_output = str(path[1]) + '\n'
    for node in path[0]:
        my_output += str(node) + ' '
    with open (output_file_name, 'w') as output_file:
        output_file.write(my_output)


################################################################################################
# Run Genetic Algorithm
################################################################################################

print(time.time())
pop = create_population()

start_time = time.time()
for i in range(10000):
    pop = create_new_generation(pop)
    if i % 100 == 0:
        if time.time() - start_time > timeout:
            write_output(sort_by_fitness(pop)[0])
            print("timeout")
            exit()
        print(sort_by_fitness(pop)[0])


################################################################################################
# Testing Example Problem
################################################################################################

# [24, 19, 25, 27, 28, 22, 21, 20, 16, 17, 18, 14, 11, 10, 9, 5, 1, 0, 4, 7, 3, 2, 6, 8, 12, 13, 15, 23, 26]

# 1000, 0.1, 1, 50, 0.5 = 37497, 38540, 37330
# 1000, 0.1, 1, 50, 0.2 = 32131, 30877, 32172
# 1000, 0.3, 1, 50, 0.2 = 45929
# 1000, 0.05, 1, 50, 0.2 = 27603, 28044, 29034 # best so far
# 1000, 0.05, 1, 50, 0.1 = 28115, 28115, #best
# 1000, 0.3, 1, 50, 0.3 = 45619

# 500, 0.05, 1, 50, 0.2 = 27750, 28871, 27750 quick
# 100, 0.05, 1, 50, 0.2 = 28044, 27750, 28779 very quick
# 100, 0.01, 1, 50, 0.2 = 27603, 27603, 28867, 28115
# 100, 0.01, 1, 10, 0.2 = 28737, 28590, 28593
# 100, 0.01, 1, 80, 0.2 = 28871, 27603, 28191, 27603

# 500, 0.01, 1, 80, 0.2 = 28871, 27603, 28191
# 100, 0.05, 1, 5, 0.1 = 30328.0

# 100, 0.01, 1, 50, 0.2 = 34828, 36347, 35177
# 100, 0.01, 1, 25, 0.3 = 36273, 33916, 35371
# 100, 0.1, 0.3, 80, 0 = 34925