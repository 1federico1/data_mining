import sys
sys.path.append('..')
from random import sample
from homework2_2 import HashFamilies as hf
from homework2_2.Shingle import Shingle


class MinWiseHash:
    def __init__(self, documents, number_of_hashing_functions):
        self.documents = documents
        self.number_of_hashing_functions = number_of_hashing_functions

    def get_set_of_signatures(self, shingle_size):
        random_values = sample(range(0, sys.maxsize), self.number_of_hashing_functions)
        doc_signatures = {}
        count = 1
        for doc_id in self.documents:
            print(doc_id)
            count += 1
            doc_signatures[doc_id] = get_signature(shingle_size, self.documents[doc_id], random_values)
        return doc_signatures


def get_signature(shingle_size, document, random_values):
    s = Shingle()
    doc_shingles = s.char_shingle(shingle_size, document)
    signature = []
    for i in random_values:
        hash_fun = hf.hash_family(i)
        hashes = []
        get_hashes_from_shingles(doc_shingles, hash_fun, hashes)
        signature.append(get_min(hashes))
    return signature


def get_hashes_from_shingles(doc_shingles, hash_fun, hashes):
    for shingle in doc_shingles:
        hash_i = hash_fun(shingle)
        hashes.append(hash_i)


def get_min(hashes):
    min = hashes[0]
    for hash in hashes:
        if min > hash:
            min = hash
    return min


if __name__ == '__main__':
    # create shingles of the documents
    d1 = 'document number one'
    d2 = 'document number two'
    d3 = 'a completely different document'
    documents = {'d1': d1, 'd2': d2, 'd3': d3}
    s = Shingle()
    shingles_d1 = s.char_shingle(4, d1)
    print(shingles_d1)

    random_values = sample(range(0, sys.maxsize), 100)
    sig_d1 = get_signature(4, d1, random_values)
    sig_d2 = get_signature(4, d2, random_values)
    sig_d3 = get_signature(4, d3, random_values)

    mh = MinWiseHash(documents, 100)
    print(mh.get_set_of_signatures(4))
