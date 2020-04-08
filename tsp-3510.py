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
euclidean_distance = np.sqrt(np.square(x_diff) + np.square(y_diff))  # euclidean distance formula

print(euclidean_distance[3][1])  # gets the euclidean distance between point 4 and 2



################################################################################################
# Output data to file
################################################################################################

with open (output_file_name, 'w') as output_file:
    output_file.write("Output goes here")
