from typing import List

import click

from .repository import Repository


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
