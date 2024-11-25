

class ArcRunner:
    """Runs tasks for the ARC dataset."""
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def run(self):
        if self.verbose:
            print('Arc Runner')
