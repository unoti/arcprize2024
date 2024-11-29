import pandas as pd
from typing import Optional

from arclib.infra.blob import BlobProvider, FileSystemBlobProvider
from arclib.models import Session, DialogRole, case_markdown_link
from arclib.dataproviders.case_metadata import get_case_title


class Evaluator:
    """Evaluates and summarizes the results of runs.
    """
    def __init__(self, blob: Optional[BlobProvider] = None, start_dir: Optional[str] = None):
        if start_dir:
            blob = FileSystemBlobProvider(start_dir + 'local/out')
        elif not blob:
            blob = FileSystemBlobProvider('local/out')
        self.blob = blob

    def run_list(self) -> str:
        """Returns a list of all the directory names for runs we have done, sequentially.

        A "run" is a when we ran arc_runner to produce a collection of sessions for each case.
        """
        session_filenames = sorted(self.blob.find())
        # These session filenames are across all runs.
        last_run = None
        all_runs = []
        for filename in session_filenames:
            filename = filename.replace('\\', '/')
            dirname = filename.split('/')[0]
            if last_run != dirname:
                last_run = dirname
                all_runs.append(last_run)
        return all_runs

    def last_run(self) -> str:
        """Returns the directory name of the last run."""
        return self.run_list()[-1]

    def score_run_df(self, run_dir: Optional[str] = "") -> pd.DataFrame:
        """Returns a dataframe summarizing the results of a run.
        :param run_dir: The directory of the run. If not specified uses the last run.
        """
        if not run_dir:
            run_dir = self.last_run()
        sessions_dir = run_dir + '/sessions/'
        session_filenames = self.blob.find(sessions_dir)
        recs = []
        for session_filename in session_filenames:
            rec = self._process_session(session_filename)
            recs.append(rec)
        df = pd.DataFrame(recs).set_index('case_id').sort_values(by=['case_id'])
        return df

    def score_run_markdown(self, run_dir: Optional[str] = "") -> str:
        """Score a recent run and return the results as a markdown string."""
        df = self.score_run_df(run_dir)
        # Humanize it a bit.
        success_percent = sum(df.success) / len(df) * 100
        df.success = df.success.apply(lambda t: None if t is None else 'PASS' if t else 'fail')
        df = df.rename(columns={
            'session_id': 'Session',
            'success': 'Result',
            'title': 'Title',
            'case_url': 'Link',
            })
        df.index.names = ['Case']

        summary = f'## Run Results\nSuccess rate: **{success_percent:0.1f}%**\n\n'
        result = summary + df.to_markdown()
        return result

    def _process_session(self, session_filename: str) -> dict:
        content = self.blob.load(session_filename)
        session = Session.from_json(content)
        case_id = session.app_context.get('case_id')
        rec = {
            'case_id': case_id,
            'session_id': session.id,
            'success': session.app_context.get('success'),
            'title': get_case_title(case_id),
            #'step_count': len(session.dialog.as_tuples(DialogRole.USER)),
            'case_url': case_markdown_link(case_id),
        }
        return rec


def main():
    evaluator = Evaluator()
    print(evaluator.score_run_markdown())


if __name__ == '__main__':
    main()