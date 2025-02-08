from typing import LiteralString
import string
import random


def generate_password(
    length: int,
    population: LiteralString = string.ascii_lowercase
    + string.ascii_uppercase
    + string.digits
    + string.punctuation,
):
    return "".join(random.choice(population) for _ in range(length))
