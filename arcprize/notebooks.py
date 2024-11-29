"""Helpful functions for working in notebooks."""
from IPython.display import display, Markdown


from arcprize.evaluation import Evaluator

def show_markdown(s: str):
    return display(Markdown(s))

def evaluate_run():
    """Evaluate the last run we did and return the results as a markdown table in a notebook.
    """
    evaluator = Evaluator(start_dir='../../') # Back up to root directory.
    table_str = evaluator.score_run_markdown()
    return show_markdown(table_str)
