from functools import reduce
from random import randrange


def generate_12_random_numbers():
    numbers = []
    for x in range(12):
        numbers.append(randrange(10))
    return numbers


def generate_random_ean():
    numbers = generate_12_random_numbers()
    assert len(numbers) == 12, "EAN must be a list of 12 numbers"
    sum_ = lambda x, y: int(x) + int(y)
    evensum = reduce(sum_, numbers[::2])
    oddsum = reduce(sum_, numbers[1::2])
    numbers.append((10 - ((evensum + oddsum * 3) % 10)) % 10)
    return ''.join(map(str, numbers))


def calculate_ean(number):
    digits = [int(x) for x in str(number)]
    assert len(digits) == 12, "EAN must be a list of 12 numbers"
    sum_ = lambda x, y: int(x) + int(y)
    evensum = reduce(sum_, digits[::2])
    oddsum = reduce(sum_, digits[1::2])
    digits.append((10 - ((evensum + oddsum * 3) % 10)) % 10)
    result = ""
    for i in digits:
        result += str(i)
    return int(result)


# calculate_ean(457389382479)
# print(generate_random_ean())
