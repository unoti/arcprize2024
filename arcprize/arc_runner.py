from arclib.core import AgentSystem

class ArcRunner:
    """Runs tasks for the ARC dataset."""
    def __init__(self,
                 agent_system: AgentSystem,
                 verbose=False):
        self.agent_system = agent_system
        self.verbose = verbose
    
    def run(self):
        if self.verbose:
            print('Arc Runner')
        self.agent_system.run()