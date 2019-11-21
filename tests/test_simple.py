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
def bash_filetree(bash, log):
    '''Create filetree in bash session'''
    log.debug('Creating bash_filetree')
    root = Path(bash.tmpdir)
    for dirname in DIRS:
        (root / dirname).mkdir(parents=True)
    for filename in FILES:
        (root / filename).touch()
    yield bash
    log.debug('Destroying bash_filetree')


class TestSimpleCompletion:
    '''All tests in this class will run within the same instance of bash'''

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
    def test_simple_one_result(self, bash_filetree, command, completion):
        '''Complete unambiguos paths - default completer'''
        bash = bash_filetree
        assert bash.complete(command) == completion


    @pytest.mark.parametrize(
        'command,completions',
        (
            ('ls usr/s', ['usr/share', 'usr/somefile']),
            ('ls usr/', ['share/', 'somefile']),
            ('cd usr/share/a', ['usr/share/another', 'usr/share/anything', 'usr/share/applications']),
            ('cd usr/share/', ['usr/share/another', 'usr/share/anything', 'usr/share/applications']),
        )
    )
    def test_simple_many_results(self, bash_filetree, command, completions):
        '''Complete ambiguous paths - default completer'''
        bash = bash_filetree
        completed = bash.complete(command)
        assert completed
        for variant in completions:
            assert variant in completed


    @pytest.mark.parametrize(
        'command,completion',
        (
            ('ls u/s/app', 'ls usr/share/applications'),
            ('cd u/s', 'cd usr/share'),
        )
    )
    def test_bcpp_one_result(self, bash_filetree, command, completion):
        '''Complete unambiguios paths - partial completer'''
        bash = bash_filetree
        assert bash.complete(command) == completion


def test_debug(bash_filetree):
    bash = bash_filetree
    import pdb; pdb.set_trace()
