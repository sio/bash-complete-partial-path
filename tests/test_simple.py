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


@pytest.fixture(scope='class')
def bash_filetree(bash):
    '''Create filetree in bash session'''
    root = Path(bash.tmpdir)
    for dirname in DIRS:
        (root / dirname).mkdir(parents=True)
    for filename in FILES:
        (root / filename).touch()
    yield bash


class TestSimpleCompletion:
    @pytest.mark.parametrize(
        'command,completion',
        (
            ('ls us', 'r'),
            ('cd us', 'r'),
            ('ls usr/sha', 're'),
            ('ls ', 'usr/'),
            ('cd usr/', 'share'),
        )
    )
    def test_simple_one_result(bash_filetree, command, completion):
        bash = bash_filetree
        assert bash.complete(command) == completion
