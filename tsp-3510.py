import sys

input_file_name = sys.argv[1]  # inputfilename.txt
output_file_name = sys.argv[2]  # outputfilename.txt
time = sys.argv[3]  # a rational number greater than 0

# example: $ python3.7 tsp-3510.py mat-test.txt output.txt 5

with open (input_file_name, 'r') as input_file:
    input_data = input_file.read()
    print(input_data)

with open (output_file_name, 'w') as output_file:
    output_file.write("Output goes here")
