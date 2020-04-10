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


def generate_route():
    return random.sample(range(len(coordinates)), len(coordinates))


def get_route_length(route):
    route_length = 0
    for i in range(len(route)):
        route_length += euclidean_distance[route[i]][route[(i + 1) % len(route)]]
    return route_length


def create_population(population_size):
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


pop = create_population(10)
pop = sort_by_fitness(pop)
print(pop[0])
print(pop[1])
print(breed(pop[0], pop[1]))

################################################################################################
# Output data to file
################################################################################################

with open (output_file_name, 'w') as output_file:
    output_file.write("Output goes here")
