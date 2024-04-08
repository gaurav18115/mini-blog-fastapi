import random
import string


def generate_unique_id():
    # Generate three random 3-letter words
    words = [''.join(random.choices(string.ascii_lowercase, k=3)) for _ in range(3)]

    # Join the words with hyphens
    id_string = "-".join(words)

    # Generate a 5-digit random number and append it to the ID string
    id_number = random.randint(100, 999)
    unique_id = f"{id_string}-{id_number}"

    return unique_id

