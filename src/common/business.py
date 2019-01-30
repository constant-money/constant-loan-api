import random
import string

from django.utils import timezone


def get_now():
    now = timezone.now()
    # if not timezone.is_naive(now):
    #     now = timezone.make_naive(now, timezone.utc)

    return now


def generate_random_code(n: int):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))


def generate_random_digit(n: int):
    return ''.join(random.choices(string.digits, k=n))
