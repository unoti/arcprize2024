import random
import string

def random_string(length=8):
    """Generates a random printable string."""
    return ''.join(random.sample(string.ascii_lowercase + string.digits, length))