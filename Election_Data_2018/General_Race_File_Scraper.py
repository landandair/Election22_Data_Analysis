import numpy as np
import csv

state_list = ('AZ', 'MI', 'OH', 'PA', 'WA')
state_info = {}
for state in state_list:
    state_info[state] = []
with open('SENATE_precinct_general.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        state_name = line[19]
        if state_list.__contains__(line[19]):
            state_info[state_name].append(line)

for state in state_info.keys():
    with open('SENATE2018_precinct_' + state + '.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(state_info[state])
        print(state_info[state])
