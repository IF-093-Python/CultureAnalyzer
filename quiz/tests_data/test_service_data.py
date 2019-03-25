import random

NUMBER_OF_QUESTION = 24

INVALID_MIN_VALUE = -100
INVALID_MAX_VALUE = 200

VALID_MIN_VALUE = 0
VALID_MAX_VALUE = 100


def get_random_data(min_data, max_data, number_of_question):
    return [random.randint(min_data, max_data) for _ in
            range(number_of_question + 1)]


def get_group_random_data(min_data, max_data, number_of_question):
    users_in_groups = random.randint(10, 100)
    return [
        get_random_data(min_data, max_data, number_of_question) for _ in
        range(users_in_groups)]
