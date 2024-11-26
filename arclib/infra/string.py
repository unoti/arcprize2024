import random
import string
import textwrap
from typing import List

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

def indent_rows(rows: List[str], count: int) -> List[str]:
    """Add a given number of spaces in front of a list of strings to a new list."""
    if count <= 0:
        return rows
    space_str = spaces(count)
    return [space_str + s for s in rows]

def spaces(count: int) -> str:
    """Make a given number of spaces."""
    return ' ' * count

def make_comma(comma: bool) -> str:
    """Conditionally create a comma."""
    if comma:
        return ','
    else:
        return ''
