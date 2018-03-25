from typing import Dict, List

import yaml


def load_config(fname: str) -> Dict:
    with open(fname) as fd:
        return yaml.load(fd)


def expand_commit_range(crange: str, commits: List[str]) -> List[str]:
    com1, com2 = crange.split('..')
    idx1, idx2 = commits.index(com1), commits.index(com2)
    return commits[idx1:idx2+1]
