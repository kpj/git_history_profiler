import os

import pytest

from ..utils import *


@pytest.fixture
def tempconfig(tmpdir):
    fname = os.path.join(tmpdir, 'config.yaml')
    with open(fname, 'w') as fd:
        fd.write('working_directory: tmp')
    return fname

def test_config(tempconfig):
    config = load_config(tempconfig)
    assert config['working_directory'] == 'tmp'

def test_crange_expansion():
    res = expand_commit_range('b..d', ['a', 'b', 'c', 'd', 'e'])
    assert res == ['b', 'c', 'd']
