import string, random


def generate_random_string(N):
    res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))
    return res

