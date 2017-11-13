from homework2_2 import HashFamily
from homework2_2.Shingle import Shingle


class MinWiseHash:

    def __init__(self, documents, values):
        """
        :param documents: the set of documents to which we have to apply the minwise hash technique
        :param values: is the range of numbers to use for creating the hashing functions. You may want to use a random
        set of values or a range of integers (i.e. range(0, 100))
        """
        self.documents = documents
        self.values = values

    def get_set_of_signatures(self, shingle_size):
        doc_signatures = {}
        count = 1
        print('Computing signatures of length ' + str(self.values[-1] + 1))
        for doc_id in self.documents:
            print('computing signature of document number ' + str(doc_id))
            count += 1
            doc_signatures[doc_id] = self.get_signature(shingle_size, self.documents[doc_id])
        return doc_signatures

    def get_signature(self, shingle_size, document):
        s = Shingle(document)
        doc_shingles = s.char_shingle(shingle_size)
        signature = []
        hf = HashFamily.HashFamily()
        for i in self.values:
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
    min_hash = hashes[0]
    for hash in hashes:
        if min_hash > hash:
            min_hash = hash
    return min_hash
