from typing import Dict

import yaml


def load_config(fname: str) -> Dict:
    with open(fname) as fd:
        return yaml.load(fd)
