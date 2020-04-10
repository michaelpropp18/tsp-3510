import random
import sys
import numpy as np

################################################################################################
# Load Command Line Arguments and Data
################################################################################################

input_file_name = sys.argv[1]  # inputfilename.txt
output_file_name = sys.argv[2]  # outputfilename.txt
time = sys.argv[3]  # a rational number greater than 0

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
# Genetic Algorithm
################################################################################################


# 0.1, 1, 50, 0.5 = 37497, 38540, 37330
# 0.1, 1, 50, 0.2 = 32131, 30877, 32172
# 0.3, 1, 50, 0.2 = 45929
# 0.05, 1, 50, 0.2 = 27603, 28044, 29034
# 0.05, 1, 50, 0.1 = 28115, 28115,
population_size = 1000  # number of routes in each population iteration
individual_mutation_rate = 0.05  # proportion of cities that are randomly changed in a route mutation
population_mutation_rate = 1  # proportion of routes that mutate each iteration
elite_size = 50  # size of population guaranteed to survive each iteration
survival_rate = 0.1  # rate of survival for not elite population each iteration


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


'''
pop = create_population(10)
pop = sort_by_fitness(pop)
print(pop[0])
print(pop[1])
print(breed(pop[0], pop[1]))
'''
pop = create_population()
for i in range(1000):
    pop = create_new_generation(pop)
    if i % 100 == 0:
        print(sort_by_fitness(pop)[0])


################################################################################################
# Output data to file
################################################################################################

with open (output_file_name, 'w') as output_file:
    output_file.write("Output goes here")
