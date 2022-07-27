import numpy as np

Desired_Races = ('AL7', 'VA2', 'CA2')  # Put districts you want a list of zip codes for
dist_to_zips = {}  # Correlation between the district and the zip codes for it
zip_to_dist = {}
for race in Desired_Races:  # (Sets default)
    dist_to_zips[race] = []
conversion = np.loadtxt('US_ZIP_Congress_Dist.csv', dtype=str, delimiter=',')

for line in conversion[1:]:
    id = line[1] + str(line[3])  # Makes district from file
    if Desired_Races.__contains__(id):
        dist_to_zips[id].append(line[2])  # Adds to the dictionary
    zip_to_dist[line[2]] = id


print(zip_to_dist)
