'''
Simple completion cases for file and directory paths
'''

import pytest


class TestPathCompletion:
    '''All tests in this class will run within the same instance of bash'''

    @pytest.mark.parametrize(
        'command,completion',
        (
            # Default completer
            ('ls us', 'r'),
            ('cd us', 'r'),
            ('ls usr/sha', 're'),
            ('ls ', 'usr/'),
            ('cd usr/', 'share'),

            # Partial path completer
            ('ls u/s/app', 'ls usr/share/applications'),
            ('cd u/s', 'cd usr/share'),
        )
    )
    def test_one_result(self, bash, command, completion):
        '''Complete unambiguos paths'''
        assert bash.complete(command) == completion


    @pytest.mark.parametrize(
        'command,variants',
        (
            # Default completer
            ('ls usr/s', ['usr/share', 'usr/somefile']),
            ('ls usr/', ['share/', 'somefile']),
            ('cd usr/share/a', ['usr/share/another', 'usr/share/anything', 'usr/share/applications']),
            ('cd usr/share/', ['usr/share/another', 'usr/share/anything', 'usr/share/applications']),

            # Partial path completer
            ('ls u/s/a', ['usr/share/afile', 'usr/share/another', 'usr/share/anything', 'usr/share/applications']),
            ('cd u/s/a', ['usr/share/another', 'usr/share/anything', 'usr/share/applications']),
        )
    )
    def test_many_results(self, bash, command, variants):
        '''Complete ambiguous paths'''
        completed = bash.complete(command)
        assert completed, 'empty completion'
        for variant in variants:
            assert variant in completed
        for variant in variants:
            completed = completed.replace(variant, '')
        assert not completed.strip(), 'extra output in completion results'
