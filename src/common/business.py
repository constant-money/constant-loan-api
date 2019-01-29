import random
import string


def generate_random_code(n: int):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))


def generate_random_digit(n: int):
    return ''.join(random.choices(string.digits, k=n))
