import random
import string

def random_token(size=100):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

def random_uid():
    ''.join(random.choice(string.hexdigits) for _ in range(32))
