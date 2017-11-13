import csv
import time
from collections import defaultdict
from itertools import combinations
from homework2_2.MinwiseHash import MinWiseHash
import os
import re

threshold = .8


class LocalitySensitiveHashing:
    def __init__(self, documents, number_of_bands, shingle_size, lsh_hash_function,
                 minwise_range_of_values):
        """

        :param documents: the documents we want to compare for similarity
        :param number_of_bands: the number of bands to which we want to divide the minhashes of documents. The row of
        each band is a direct result of this parameter
        :param number_of_hashing_functions: the number of hashing functions we want to use for hash the documents with
        the minwise hash technique
        :param shingle_size: the size of the documents' shingles
        :param lsh_hash_function: the hashing function used for hashing the bands to the buckets.
        :param minwise_range_of_values: the range of values used for generating the families of hashes for the minwise
        hash
        """
        self.number_of_bands = number_of_bands
        self.rows = 0
        self.documents = documents
        self.lsh_hash_function = lsh_hash_function
        self.mw = MinWiseHash(self.documents, minwise_range_of_values)
        self.signatures = {}

        if os.path.isfile('signatures.txt'):
            with open('signatures.txt', 'r') as sign_file:
                sign_file = csv.reader(sign_file, delimiter='\t')
                for row in sign_file:
                    hashes = re.sub('\W+', ' ', row[1]).split()
                    self.signatures[row[0]] = hashes
        else:
            start_time_signatures = time.time()
            self.signatures = self.mw.get_set_of_signatures(shingle_size)
            print('time to compute signatures: ' + str((time.time() - start_time_signatures)/60) + ' minutes')
            with open('signatures.txt', 'w') as sign_file:
                for doc_id in self.signatures:
                    sign_file.write(str(doc_id))
                    sign_file.write('\t')
                    sign_file.write(str(self.signatures[doc_id]))
                    sign_file.write('\n')

    def split_signature_in_bands(self, signature):
        if self.number_of_bands in get_divisors(len(signature)):
            self.rows = int(len(signature) / self.number_of_bands)
            signature = [signature[x:x + self.rows] for x in range(0, len(signature), self.rows)]
            return signature
        else:
            print('you may want to use this values for the number of bands: ' + str(get_divisors(len(signature))))
            raise Exception()

    def split_all_docs(self):
        docs2bands = {}
        for doc_id in self.documents:
            docs2bands[doc_id] = self.split_signature_in_bands(self.signatures[doc_id])
        return docs2bands

    def get_hash_map(self):
        hash_map = defaultdict(list)
        split_docs = self.split_all_docs()
        print('Number of bands = ' + str(self.number_of_bands))
        print('Number of rows per band = ' + str(self.rows))
        for doc_id in split_docs:
            for band in split_docs[doc_id]:
                hash_band = self.lsh_hash_function(implode(band))
                hash_map[hash_band].append(doc_id)
        return hash_map

    def get_candidates(self):
        hash_map = self.get_hash_map()
        candidates = {}
        je = JaccardEstimation()
        for hask_key in hash_map:
            values = combinations(hash_map[hask_key], 2)
            for t0, t1 in values:
                est = je.get_jaccard_estimation(sorted(self.signatures[t0]), sorted(self.signatures[t1]))
                if est >= threshold:
                    candidates[(t0, t1)] = est
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


class NearestNeighbors:
    def __init__(self, shingles):
        self.shingles = shingles

    def compute_nearest(self):
        output = {}
        je = JaccardEstimation()
        tmp = '0'
        for doc_0, doc_1 in combinations(self.shingles.keys(), 2):
            est = je.get_jaccard_estimation(self.shingles[doc_0], self.shingles[doc_1])
            if est >= threshold:
                output[(doc_0, doc_1)] = est
            if tmp != doc_0:
                print('processing nearest neighbors of document ' + doc_0)
                tmp = doc_0
        return output


class JaccardEstimation:
    @staticmethod
    def get_jaccard_estimation(vector_1, vector_2):
        """
        computes the jaccard similarity between two SORTED vectors. We use sorted vectors because we can arrange a
        better result in terms of complexity. 
        :param vector_1:
        :param vector_2:
        :return:
        """
        intersection = 0
        i = j = 0
        while i < len(vector_1) and j < len(vector_2):
            if vector_1[i] == vector_2[j]:
                intersection += 1
                i += 1
                j += 1
            elif vector_1[i] < vector_2[j]:
                i += 1
            else:
                j += 1
        return intersection / (len(vector_1) + len(vector_2) - intersection)
