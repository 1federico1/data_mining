import hashlib


class HashFamily:
    @staticmethod
    def hash_family(i):
        result_size = 8
        max_len = 20
        salt = str(i).zfill(max_len)[-max_len:]

        def hash_member(x):
            return hashlib.sha1(str(x + salt).encode('utf-8')).hexdigest()[-result_size:]

        return hash_member
