import random
import string

def generate_unique_code(length=5):
    letters = string.ascii_letters  # Uppercase and lowercase letters
    return ''.join(random.choice(letters) for _ in range(length))
