import os
import time
import shutil
from io import StringIO

from typing import Optional, List

import sh
import click

import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from tqdm import tqdm

from .utils import load_config


class Repository:
    def __init__(self, url: str, config: str) -> None:
        self.url = url

        self.config_dir = os.path.dirname(config)
        self.config = load_config(config)
        os.makedirs(self.config['working_directory'])

    @property
    def repo_dir(self) -> str:
        return os.path.abspath(os.path.join(
            self.config['working_directory'], 'repo'))

    @property
    def results_dir(self) -> str:
        return os.path.abspath(os.path.join(
            self.config['working_directory'], 'result_cache'))

    def clone(self) -> None:
        if os.path.exists(self.url):
            # is local
            shutil.copytree(self.url, self.repo_dir)
        else:
            # is remote
            sh.git.clone(
                self.url, 'repo',
                _cwd=self.config['working_directory'])

    def clean(self) -> None:
        sh.git.clean('-f', '-d', _cwd=self.repo_dir)

    def switch_to_commit(self, commit_id: str) -> None:
        # switch to commit
        sh.git.checkout(commit_id, _cwd=self.repo_dir)

        # prepare environment
        cmd_path = os.path.join(self.config_dir, self.config['init_script'])
        os.system(f'{cmd_path} "{self.repo_dir}" > /dev/null')

    def execute(self, commit_id: str) -> List:
        stats = []
        for job in tqdm(self.config['jobs'], desc='Jobs'):
            cmd_path = os.path.join(self.config_dir, job['command'])
            # cmd = sh.Command(cmd_path)

            # time command
            start = time.time()
            # cmd(_cwd=self.repo_dir)
            os.system(f'cd "{self.repo_dir}" && {cmd_path} > /dev/null')
            dur = time.time() - start

            # handle results
            result_files = []
            result_cache = os.path.join(
                self.results_dir, commit_id, job['name'].replace(' ', '_'))
            os.makedirs(result_cache)
            for fname in job['files']:
                fpath = os.path.join(self.repo_dir, fname)
                rpath = os.path.join(result_cache, fname)

                os.makedirs(os.path.dirname(rpath), exist_ok=True)
                shutil.copy(fpath, rpath)
                result_files.append((fname, rpath))

            stats.append((commit_id, job['name'], dur, result_files))
        return stats

    def handle_commit(self, commit_id: str) -> List:
        self.clean()
        self.switch_to_commit(commit_id)
        return self.execute(commit_id)

    def list_commits(self) -> List[str]:
        buf = StringIO()
        sh.git(
            'rev-list', '--all', '--reverse', _out=buf,
            _cwd=self.repo_dir)
        return buf.getvalue().split()

    def parse_commits(self, commits: Optional[List[str]]) -> List[str]:
        all_commits = self.list_commits()
        if commits is None:
            return all_commits

        new_commits = []
        for commit in commits:
            if '..' in commit:
                com1, com2 = commit.split('..')
                idx1, idx2 = all_commits.index(com1), all_commits.index(com2)
                new_commits.extend(all_commits[idx1:idx2+1])
            else:
                new_commits.append(commit)

        return new_commits

    def run(self, commits: Optional[List[str]] = None) -> List:
        self.clone()

        stats = []
        commits = self.parse_commits(commits)

        for commit in tqdm(commits, desc='Commit history'):
            res = self.handle_commit(commit)
            stats.extend(res)

        df = pd.DataFrame(
            stats,
            columns=['commit', 'job', 'time', 'result_files'])
        df.to_csv(
            os.path.join(self.config['working_directory'], 'raw.csv'),
            index=False)
        return df

    def plot(self, df: pd.DataFrame) -> None:
        # plot
        plt.figure()
        sns.pointplot(x='commit', y='time', hue='job', data=df)

        plt.xticks(rotation=90)
        plt.gca().set_xticklabels(
            [item.get_text()[:7] for item in plt.gca().get_xticklabels()])

        plt.xlabel('Commits [id]')
        plt.ylabel('Execution time [s]')
        plt.title('Performance overview')

        plt.tight_layout()
        plt.savefig(os.path.join(
            self.config['working_directory'], 'performance.pdf'))

    def compare_results(self, df: pd.DataFrame) -> None:
        # gather data
        data = []
        for row in df.itertuples():
            for fname, fpath in row.result_files:
                fsize = os.path.getsize(fpath)
                data.append((row.commit, fname, fsize))
        df = pd.DataFrame(data, columns=['commit', 'result_file', 'size'])

        # plot result
        plt.figure()
        sns.pointplot(x='commit', y='size', hue='result_file', data=df)

        plt.xticks(rotation=90)
        plt.gca().set_xticklabels(
            [item.get_text()[:7] for item in plt.gca().get_xticklabels()])

        plt.xlabel('Commits [id]')
        plt.ylabel('File size [bytes]')
        plt.title('Result file overview')

        plt.tight_layout()
        plt.savefig(os.path.join(
            self.config['working_directory'], 'result_overview.pdf'))


@click.command()
@click.argument('repo_url')
@click.option(
    '--config', required=True,
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help='Path to config.')
@click.option(
    '-c', '--commit', multiple=True,
    help='Commit id to consider.')
def main(repo_url: str, config: str, commit: List[str]) -> None:
    """ Performance and stability profiling over the git commit history.
    """
    repo = Repository(repo_url, config)
    df = repo.run(commit if len(commit) > 0 else None)

    repo.plot(df)
    repo.compare_results(df)


if __name__ == '__main__':
    main()
