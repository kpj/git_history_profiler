# GitHistoryProfiler

Performance and and stability profiling over the git commit history.

## Usage

```bash
$ python main.py --help
Usage: main.py [OPTIONS] REPO_URL

  Performance and and stability profiling over the git commit
  history.

Options:
  --config PATH      Path to config.  [required]
  -c, --commit TEXT  Commit id to consider.
  --help             Show this message and exit.
```

Try out the example:
```bash
$ examples/create_test_repository.sh test_repo
$ python main.py test_repo --config examples/config.yml
```
