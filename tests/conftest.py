'''
Shared fixtures for completion testing
'''

import os
import platform
import re
from itertools import chain
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
import pexpect


if platform.system() == 'Windows':  # ptys are not available in Windows
    raise RuntimeError('Automated tests can not be executed on Windows '
        'because underlying tooling is not available yet: '
        'https://pexpect.readthedocs.io/en/stable/overview.html#pexpect-on-windows'
    )


class BashSessionError(Exception):
    '''Raised by BashSession when bash encounters unhandled error'''


class BashSession:
    '''Wrapper for interactive bash session'''

    ENCODING = 'utf-8'
    MARKER = '>>-!-<<'
    PS1 = '__>>>__'
    STARTUP = [
        "bind 'set bell-style none'",
    ]

    def __init__(self, *a,
                 cmd='bash',
                 args='--norc --noprofile',
                 env=None,
                 startup=None,
                 **ka):
        if a:
            raise ValueError('only keyword arguments are supported')
        environment = os.environ.copy()
        if env:
            environment.update(env)
        environment.update(dict(
            PS1=self.PS1,
            TERM='dumb',
        ))
        self.process = pexpect.spawn(
            '{} {}'.format(cmd, args),
            env=environment,
            encoding=self.ENCODING,
            dimensions=(24, 160),  # https://github.com/scop/bash-completion/blob/fb46fed657d6b6575974b2fd5a9b6529ed2472b7/test/t/conftest.py#L112-L115
            **ka,
        )
        for command in chain(self.STARTUP, startup or ()):
            self.execute(command)

    def complete(self, text, tabs=1):
        '''
        Trigger completion after inputting text into interactive bash session

        Return completion results
        '''
        self._clear_current_line()

        proc = self.process
        proc.send('{}{}'.format(text, '\t' * tabs))
        proc.expect_exact(text)
        proc.send(self.MARKER)
        result = proc.expect([
            re.escape(self.MARKER),
            self.PS1,
        ])
        output = proc.before.strip()

        proc.sendcontrol('c')  # drop current input
        proc.expect_exact(self.PS1)
        return output

    def execute(self, command, timeout=-1, exitcode=0):
        '''
        Execute a single command in interactive shell. Check its return code.

        Return terminal output after execution.
        '''
        self._clear_current_line()

        proc = self.process
        proc.sendline(command)
        proc.expect_exact(command, timeout=timeout)
        proc.expect_exact(self.PS1, timeout=timeout)
        output = proc.before.strip()

        echo = 'echo "$?"'
        proc.sendline(echo)
        proc.expect_exact(echo, timeout=timeout)
        proc.expect_exact(self.PS1, timeout=timeout)
        returned = proc.before.strip()
        if str(exitcode) != returned:
            message = '{command} exited with code {returned} (expected {exitcode})\n{output}'
            raise BashSessionError(message.format(**locals()))

        return output

    def _clear_current_line(self):
        '''Clear any input on the current line <https://askubuntu.com/a/471023>'''
        self.process.sendcontrol('e')
        self.process.sendcontrol('u')


BCPP = 'bash_completion'  # relative path from repo's top level


@pytest.fixture(scope='class')
def bash() -> BashSession:
    '''
    Fixture for automated tests.

    Provides BashSession object initialized in a temporary directory with bcpp
    preloaded. Temp directory is cleaned up automatically
    '''
    startup = [
        'source "{}"'.format(Path(BCPP).resolve()),
        '_bcpp --defaults',
    ]
    with TemporaryDirectory(prefix='bcpp_test_') as tmpdir:
        shell = BashSession(
            startup=startup,
            cwd=tmpdir,
        )
        shell.tmpdir = tmpdir
        yield shell
