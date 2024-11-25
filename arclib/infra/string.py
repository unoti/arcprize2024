import random
import string
import textwrap

def random_string(length=8):
    """Generates a random printable string."""
    return ''.join(random.sample(string.ascii_lowercase + string.digits, length))


def dedent(s: str) -> str:
    """Remove leading and trailing spaces from a multi-line string.
    
    This lets you use docstrings for strings, reducing their fixed indent
    but retaining indentation relative to the second line.
    """
    lines = s.split('\n')
    if len(lines) == 0:
        return ''
    if len(lines) == 1:
        return s
    first = lines[0]
    rest = '\n'.join([line.rstrip() for line in lines[1:]])
    result = first + '\n' + textwrap.dedent(rest)
    return result