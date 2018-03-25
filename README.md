# git_history_profiler

[![PyPI](https://img.shields.io/pypi/v/git_history_profiler.svg?style=flat)](https://pypi.org/project/git-history-profiler/)
[![Build Status](https://travis-ci.org/kpj/git_history_profiler.svg?branch=master)](https://travis-ci.org/kpj/git_history_profiler)

Performance and stability profiling over the git commit history.

## Installation

```bash
$ pip install git_history_profiler
```

## Usage

```bash
$ git_history_profiler --help
Usage: git_history_profiler [OPTIONS] REPO_URL

  Performance and stability profiling over the git commit history.

Options:
  --config PATH      Path to config.  [required]
  -c, --commit TEXT  Commit id to consider.
  --help             Show this message and exit.
```

Try out the example:
```bash
$ ./examples/create_test_repository.sh ./test_repo/
$ git_history_profiler ./test_repo/ --config ./examples/config.yml
```
Afterwards, check out `./profiling_results/`.
