from homework2_2 import HashFamily


jobs_announcementes = '../homework2_1/jobs.tsv'


class Shingle:
    def __init__(self, document):
        """
        :param document: the document we want to obtain the shingles
        """
        self.document = document

    def char_shingle(self, k):
        """
        :param k: number of shingles we want to divide the char
        :return: a list representing the char divided in k-shingles
        """
        if len(self.document) <= k:
            return self.document
        words = []
        for i in range(len(self.document)):
            shingle = self.document[i:i + k]
            if len(shingle) == k:
                words.append(shingle)
        return words

    def hash_shingles(self, k, hash_function):
        """
        :param k: number of shingles we want to divide the char
        :param hash_function: the hash function we want to use to hash the shingles
        :return: a list representing the char divided in hashes of the k-shingles representing it
        """
        hashes = []
        words = self.char_shingle(k)
        for word in words:
            hashes.append(hash_function(word))
        return hashes