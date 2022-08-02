from functools import reduce
from random import randrange

def generate_12_random_numbers():
    numbers = []
    for x in range(12):
        numbers.append(randrange(10))
    return numbers

def calculate_checksum(ean):
    assert len(ean) == 12, "EAN must be a list of 12 numbers"
    sum_ = lambda x, y: int(x) + int(y)
    evensum = reduce(sum_, ean[::2])
    oddsum = reduce(sum_, ean[1::2])
    return (10 - ((evensum + oddsum * 3) % 10)) % 10

numbers = generate_12_random_numbers()
numbers.append(calculate_checksum(numbers))
print(''.join(map(str, numbers)))