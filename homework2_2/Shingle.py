from homework2_2 import HashFamilies

jobs_announcementes = '../homework2_1/jobs.tsv'


class Shingle:
    def __init__(self, document):
        self.document = document

    def char_shingle(self, k):
        if len(document) <= k:
            return self.document
        words = []
        for i in range(len(self.document)):
            shingle = self.document[i:i + k]
            if len(shingle) == k:
                words.append(shingle)
        return words

    def hash_shingles(self, k, hash_fun):
        hashes = []
        words = self.char_shingle(k)
        for word in words:
            hashes.append(hash_fun(word))
        return hashes


if __name__ == '__main__':
    document = 'document number one'
    s = Shingle(document)
    shingles = s.char_shingle(4)
    print(shingles)
    hf = HashFamilies.HashFamily()
    hash_fun = hf.hash_family(23)
    hashes = s.hash_shingles(4, hash_fun)
    print(hashes)
