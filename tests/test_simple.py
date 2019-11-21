'''
Simple completion cases should be consistent with default behavior
'''

from pathlib import Path
import pytest


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
    def test_simple_one_result(self, bash, command, completion):
        '''Complete unambiguos paths - default completer'''
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
    def test_simple_many_results(self, bash, command, completions):
        '''Complete ambiguous paths - default completer'''
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
    def test_bcpp_one_result(self, bash, command, completion):
        '''Complete unambiguios paths - partial completer'''
        assert bash.complete(command) == completion


def test_debug(bash):
    import pdb; pdb.set_trace()
