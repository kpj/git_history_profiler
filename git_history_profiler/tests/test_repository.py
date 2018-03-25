import os

import pytest

from ..repository import Repository


def get_all_files(path):
    all_files = []
    for root, subdirs, files in os.walk(path):
        if root[len(path)+1:].startswith('.'):
            continue

        all_files.extend(subdirs)
        all_files.extend(files)
    return set(all_files)

@pytest.fixture
def repo(tmpdir):
    # create repository
    os.system(f'./examples/create_test_repository.sh "{tmpdir}/test_repo/"')

    # create config
    with open(f'{tmpdir}/config.yml', 'w') as fd:
        fd.write(f'working_directory: {tmpdir}/profiling_results')

    # finalize
    repo = Repository(f'{tmpdir}/test_repo/', f'{tmpdir}/config.yml')
    repo.clone()
    return repo

def test_cloning(repo):
    assert os.path.isdir(repo.repo_dir)

def test_clean(repo):
    # various file-checks
    files_before = get_all_files(repo.repo_dir)

    os.makedirs(f'{repo.repo_dir}/fubar/')
    with open(f'{repo.repo_dir}/fubar/foo.txt', 'w') as fd:
        fd.write('hahaha')
    files_interm = get_all_files(repo.repo_dir)

    repo.clean()
    files_after = get_all_files(repo.repo_dir)

    # check assertions
    assert files_before | {'fubar', 'foo.txt'} == files_interm
    assert files_before == files_after

def test_commit_list(repo):
    commits = repo.list_commits()
    assert len(commits) == 3
