'''
Simple completion cases should be consistent with default behavior
'''

from pathlib import Path
import pytest


FILES = [
    'usr/somefile',
    'usr/share/afile',
]
DIRS = [
    'usr/share/applications',
    'usr/share/another',
    'usr/share/anything',
]


@pytest.fixture
def bash_filetree(bash):
    '''Create filetree in bash session'''
    root = Path(bash.tmpdir)
    for dirname in DIRS:
        (root / dirname).mkdir(parents=True)
    for filename in FILES:
        (root / filename).touch()
    yield bash


def test_simple_one_result(bash_filetree):
    bash = bash_filetree
    for command, completion in (
            ('ls us', 'r'),
            ('cd us', 'r'),
            ('ls usr/sha', 're'),
            ('ls ', 'usr/'),
            ('cd usr/', 'share'),
    ):
        assert bash.complete(command) == completion
