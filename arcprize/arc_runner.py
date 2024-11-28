from arclib.core import AgentSystem, AgentSystemEventType, AgentSystemEvent

class ArcRunner:
    """Runs tasks for the ARC dataset."""
    def __init__(self,
                 agent_system: AgentSystem,
                 verbose=False):
        self.agent_system = agent_system
        self.verbose = verbose
        self.agent_system.add_event(AgentSystemEventType.TASK_STARTED, self._on_start_task)
        self.agent_system.add_event(AgentSystemEventType.TASK_FINISHED, self._on_end_task)
        self.agent_system.add_event(AgentSystemEventType.STEP_FINISHED, self._on_end_step)
        self.case_count = 0
        self.correct_count = 0
    
    def run(self):
        if self.verbose:
            print('Arc Runner')
        self.agent_system.run()

    def _on_start_task(self, event: AgentSystemEvent):
        self.case_count += 1
        case_id = event.task_assignment.app_context['case_id']
        print(f'{self.case_count}. Case {case_id}', end='', flush=True)
    
    def _on_end_task(self, event: AgentSystemEvent):
        success = event.session.app_context.get('success') # From arc_tasks.ScoringStep.
        if success is None:
            result = '[No score]'
        elif success:
            result = '[PASS]'
            self.correct_count += 1
        else:
            result = '[fail]'
        percent = self.correct_count / self.case_count * 100
        print(f'{result} {self.correct_count}/{self.case_count} = {percent:0.1f}%')

    def _on_end_step(self, event: AgentSystemEvent):
        print('.', end='', flush=True)
