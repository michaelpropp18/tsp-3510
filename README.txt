Michael Propp and Willem Taylor
mpropp6@gatech.edu and wtaylor67@gatech.edu
4/17/2020

Files Included:
Name: 10_Simulations_Output.txt
Description: The output of running 10 simulations of our algorithm for mat_test.

Name: 10_180_sec_alg_runs_output.txt
Description: The output of running our program 10 times with a 180 second timeout each time.
Note that our program is able to do many iterations of our algorithm within the allotted
180 seconds allowing us to find the optimal value for the mat_test every time even though
the algorithm itself only returns it roughly 15% of the time.

Name: tsp-3510.py
Description: Python file for our algorithm

Name: output.txt
Description: Sample output produced by our algorithm


Instructions:

Run $ python3.7 tsp-3510.py mat-test.txt output.txt 180
The program will read from mat-test.txt and output the answer to output.txt
You may need to install numpy, random, or time. In the commandline, type "pip install numpy"
You may need to update your python to python3.

Limitations:

Our parameters for the genetic algorithm were optimized for the sample mat-test problem.
While our program works on larger sets, it is much slower and might not be able to complete
a single simulation in the time frame (it will still output its best path at the timeout).

When a single simulation is taking a long time, an update is given every 10 seconds to inform
the user on the progress.
