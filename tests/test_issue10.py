'''
Tests for issue #10
https://github.com/sio/bash-complete-partial-path/issues/10
'''


import shlex
import pytest

from tests.conftest import FILETREE, STARTUP


class Test_Issue10:
    '''Share bash instance between the following tests'''

    DIR = 'usr/share'

    @pytest.mark.parametrize('command', ['cd', 'ls'])
    def test_single(self, bash, command):
        '''Check that single tab adds trailing slash to directory name'''
        completed = bash.complete('{} {}'.format(command, self.DIR))
        assert completed == '/'

    @pytest.mark.parametrize('command', ['cd', 'ls'])
    def test_double(self, bash, command):
        '''Check that double tab lists directory contents'''
        completed = bash.complete('{} {}'.format(command, self.DIR), tabs=2)
        variants = set(shlex.split(completed))
        files = set(x for x in FILETREE['files'] if x.startswith(self.DIR))
        dirs  = set(x for x in FILETREE['dirs'] if x.startswith(self.DIR))

        if command == 'ls':
            dirs = set(d + '/' for d in dirs)
            dirs.add('/')
            correct = set(x.replace(self.DIR + '/', '', 1) for x in files.union(dirs))
            assert variants == correct
        elif command == 'cd':
            dirs.add('/')
            assert variants == dirs
        else:
            assert False, 'unsupported command: {}'.format(command)


def test_aliases(bash):
    '''Do not use aliases for dependencies'''
    message = 'ALIASES MUST NOT BE INVOKED'
    bash.execute('alias rm="echo {}"'.format(message))
    for command in STARTUP:  # reinitialize bash-complete-partial-path
        bash.execute(command)
    assert bash.execute('rm --help') == message + ' --help'
    assert bash.complete('ls us') == 'r'
