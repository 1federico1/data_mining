import csv
import re
import sys
import time
import os
from pprint import pprint

sys.path.append('..')
from homework2_2.HashFamily import HashFamily
from homework2_2.LocalitySensitiveHashing import LocalitySensitiveHashing, NearestNeighbors
from homework2_2.Shingle import Shingle
import homework2_2.plotter as plotter

hf = HashFamily()
lsh_hash_fun = hf.hash_family(42)

descriptions = {}
count2url = {}
with open('../homework2_1/jobs.tsv', 'r') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    count = 1
    for row in tsvin:
        count2url[count] = row[4]
        descriptions[str(count)] = row[1]
        count += 1

shingles = {}

for doc_id in descriptions:
    s = Shingle(descriptions[doc_id])
    shingles[doc_id] = sorted(s.char_shingle(10))

print('number of descriptions: ' + str(len(descriptions)))

start = time.time()
kijiji_lsh = LocalitySensitiveHashing(descriptions, number_of_bands=10,
                                      shingle_size=10, lsh_hash_function=lsh_hash_fun,
                                      minwise_range_of_values=range(0, 100))
result = kijiji_lsh.get_candidates()

print('time to compute lsh: ' + str(time.time() - start) + ' seconds')

lsh_duplicates = {}
lsh_near_duplicates = {}
for docs in result:
    if result[docs] == 1.0:
        lsh_duplicates[docs] = result[docs]
    else:
        lsh_near_duplicates[docs] = result[docs]

golden_standard_duplicates = {}
golden_standard_near_duplicates = {}

# read from file to avoid computing again nearest neighbors
if os.path.isfile('nearest_neighbors.txt'):
    print('reading nearest neighbors from file')
    with open('nearest_neighbors.txt', 'r') as nn_file:
        nn_file = csv.reader(nn_file, delimiter='\t')
        for row in nn_file:
            docs = re.sub('\W+', ' ', row[0]).split()
            if row[1] == '1.0':
                golden_standard_duplicates[(docs[0], docs[1])] = row[1]
            else:
                golden_standard_near_duplicates[(docs[0], docs[1])] = row[1]
else:
    start_nn = time.time()
    nn = NearestNeighbors(shingles=shingles)
    nn_output = nn.compute_nearest()
    nn_time = time.time() - start_nn
    for docs in nn_output:
        if nn_output[docs] == 1.0:
            golden_standard_duplicates[docs] = nn_output[docs]
        else:
            golden_standard_near_duplicates[docs] = nn_output[docs]

    print('time to compute nearest neighbors: ' + str(nn_time/60) + ' minutes')
    print('writing nearest neighbors to file')
    
    with open('nearest_neighbors.txt', 'w') as nn_file:
        for docs in nn_output:
            nn_file.write(str(docs))
            nn_file.write('\t')
            nn_file.write(str(nn_output[docs]))
            nn_file.write('\n')

print('lsh duplicate documents')
pprint(lsh_duplicates)
print('lsh near duplicate documents')
pprint(lsh_near_duplicates)
print('nearest neighbors duplicate documents')
pprint(golden_standard_duplicates)
print('nearest neighbors near duplicate documents')
pprint(golden_standard_near_duplicates)
print('number of duplicated documents found by lsh algorithm ' + str(len(lsh_duplicates)))
print('number of similar documents found by lsh algorithm ' + str(len(lsh_near_duplicates)))
print('number of duplicated documents found by nearest neighbors algorithm ' + str(len(golden_standard_duplicates)))
print('number of similar documents found by nearest neighbors algorithm ' + str(len(golden_standard_near_duplicates)))

miss = hit = 0
for docs in golden_standard_duplicates:
    if docs not in lsh_duplicates:
        miss += 1
    else:
        hit += 1
print('duplicate documents missed by lsh algorithm = ' + str(miss))
print('size of intersection for duplicate documents = ' + str(hit))

miss = hit = 0
for docs in golden_standard_near_duplicates:
    if docs not in lsh_near_duplicates:
        miss += 1
    else:
        hit += 1
print('similar documents missed by lsh algorithm = ' + str(miss))
print('size of intersection for similar documents = ' + str(hit))

print('Plotting S-curve graph')
plotter.plot_s_curve(kijiji_lsh.number_of_bands, kijiji_lsh.rows)
