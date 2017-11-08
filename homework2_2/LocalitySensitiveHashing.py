import csv
import json
import time
from collections import defaultdict
from itertools import combinations
from homework2_2.HashFamilies import HashFamily
from homework2_2.Minwise import MinWiseHash
from homework2_2.Shingle import Shingle
import operator
import os

test_documents = {'d1': 'document number one',
                  'd2': 'document number two',
                  'd3': 'a completely different document',
                  'd4': 'document number different',
                  'd5': 'a not so completely different document',
                  'd6': 'a completely different document'}

threshold = .8


class NearestNeighbors:
    def __init__(self, shingles):
        self.shingles = shingles

    def compute_nearest(self):
        output = {}
        je = JaccardEstimation()
        tmp = 0
        for doc_0, doc_1 in combinations(self.shingles.keys(), 2):
            sorted_0 = sorted(self.shingles[doc_0])
            sorted_1 = sorted(self.shingles[doc_1])
            est = je.get_jaccard_estimation(sorted_0, sorted_1)
            output[(doc_0, doc_1)] = est
            if tmp != int(doc_0):
                print('processing nearest neighbors of document ' + doc_0)
                tmp = int(doc_0)
        return output


class JaccardEstimation:
    @staticmethod
    def get_jaccard_estimation(vector_1, vector_2):
        sorted_vector_1 = sorted(vector_1)
        sorted_vector_2 = sorted(vector_2)
        intersection = 0
        i = j = 0
        while i < len(sorted_vector_1) and j < len(sorted_vector_2):
            if sorted_vector_1[i] == sorted_vector_2[j]:
                intersection += 1
                i += 1
                j += 1
            elif sorted_vector_1[i] < sorted_vector_2[j]:
                i += 1
            else:
                j += 1
        return intersection / (len(sorted_vector_1) + len(sorted_vector_2) - intersection)


class LocalitySensitiveHashing:
    def __init__(self, documents, number_of_bands, number_of_hashing_functions, shingle_size):
        self.number_of_bands = number_of_bands
        self.rows = 0
        self.documents = documents
        self.number_of_hashing_functions = number_of_hashing_functions
        self.mw = MinWiseHash(self.documents, self.number_of_hashing_functions)
        self.signatures = {}

        if os.path.isfile('signatures.txt'):
            self.signatures = json.load(open('signatures.txt', 'r'))
        else:
            self.signatures = self.mw.get_set_of_signatures(shingle_size)
            json.dump(self.signatures, open('signatures.txt', 'w'))

    def split_signature_in_bands(self, signature):
        if self.number_of_bands in get_divisors(len(signature)):
            self.rows = int(len(signature) / self.number_of_bands)
            return [signature[x:x + self.rows] for x in range(0, len(signature), self.rows)]
        else:
            print('you may want to use this values for the number of bands: ' + str(get_divisors(len(signature))))
            raise Exception()

    def split_all_docs(self):
        docs2bands = {}
        for doc_id in self.documents:
            docs2bands[doc_id] = self.split_signature_in_bands(self.signatures[doc_id])
        return docs2bands

    def get_hash_map(self, hash_fun):
        hash_map = defaultdict(list)
        split_docs = self.split_all_docs()
        for doc_id in split_docs:
            for band in split_docs[doc_id]:
                hash_band = hash_fun(implode(band))
                hash_map[hash_band].append(doc_id)
        return hash_map

    def get_candidates_alt(self, hashing_function):
        hash_map = self.get_hash_map(hashing_function)
        candidates_alt = {}
        je = JaccardEstimation()
        for hask_key in hash_map:
            values = combinations(hash_map[hask_key], 2)
            for t0, t1 in values:
                est = je.get_jaccard_estimation(self.signatures[t0], self.signatures[t1])
                if est >= threshold:
                    candidates_alt[(t0, t1)] = est
        return candidates_alt

    def get_candidates(self, hashing_function):
        candidates = {}
        print('getting candidates')
        split_docs = self.split_all_docs()
        print('number of bands: ' + str(self.number_of_bands) + '\nnumber of rows: ' + str(self.rows))
        je = JaccardEstimation()

        for doc_id_tuple in combinations(self.documents.keys(), 2):
            for band in range(0, self.number_of_bands - 1):
                if doc_id_tuple not in candidates:
                    h1 = hashing_function(implode(split_docs[doc_id_tuple[0]][band]))
                    h2 = hashing_function(implode(split_docs[doc_id_tuple[1]][band]))
                    if h1 == h2:
                        jaccard = je.get_jaccard_estimation(self.signatures[doc_id_tuple[0]],
                                                            self.signatures[doc_id_tuple[1]])
                        if jaccard >= threshold:
                            print(str(doc_id_tuple) + ' is a candidate, computing jaccard estimation')
                            candidates[doc_id_tuple] = jaccard

                else:
                    print(str(doc_id_tuple) + ' is already a candidate, skip this iteration')
                    break
        return candidates


def get_divisors(n):
    divisors = []
    for i in range(1, int(n / 2) + 1):
        if n % i == 0:
            divisors.append(i)
    divisors.append(n)
    return divisors


def implode(lst):
    return ''.join(lst)


# lsh = localitysensitivehashing(test_documents, number_of_bands=25, number_of_hashing_functions=100, shingle_size=10)


hf = HashFamily()
hash_fun = hf.hash_family(1)

# candidates = lsh.get_candidates(hash_fun)

# print(candidates)

descriptions = {}
count2url = {}
with open('../homework2_1/jobs.tsv', 'r') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    count = 1
    for row in tsvin:
        count2url[count] = row[4]
        descriptions[str(count)] = row[1]  # alcuni url sono ripetuti
        count += 1
print('kijij')

shingles = {}
s = Shingle()
for doc_id in descriptions:
    shingles[doc_id] = s.char_shingle(10, descriptions[doc_id])

print(len(descriptions))
start = time.clock()

kijiji_lsh = LocalitySensitiveHashing(descriptions, number_of_bands=10, number_of_hashing_functions=100,
                                      shingle_size=10)

result = kijiji_lsh.get_candidates_alt(hash_fun)
print(time.clock() - start)

sorted_result = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
print(len(sorted_result))
print(time.clock() - start)

test = JaccardEstimation()

print(test.get_jaccard_estimation(['a', 'b', 'c', 'd', 'k'], ['a', 'b', 'e', 'f', 'u']))

# k_candidates = kijiji_lsh.get_candidates(hash_fun)
# sorted_candidates = sorted(k_candidates.items(), key=operator.itemgetter(1), reverse=True)
# lsh_time = time.clock() - start
# pp.pprint(sorted_candidates)
# print(len(sorted_candidates))
# print('end lsh')
# print(lsh_time)

start_nn = time.clock()
nn = NearestNeighbors(shingles=shingles)
nn_output = nn.compute_nearest()
print('end nn')
# sorted_nn = sorted(nn_output.items(), key=operator.itemgetter(1), reverse=True)
nn_time = time.clock() - start_nn
print(nn_output)
json.dump(nn_output, open('nearest_neighbors.txt', 'r'))
#
print(nn_time)
