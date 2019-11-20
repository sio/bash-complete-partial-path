import os
import platform

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
    PS1 = '__>>>__'
    ENCODING = 'utf-8'

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
        for command in (startup or ()):
            self.execute(command)

    def complete(self, text):
        pass

    def execute(self, command, timeout=-1, exitcode=0):
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
        '''
        Clear any input on the current line
        https://askubuntu.com/a/471023
        '''
        self.process.sendcontrol('e')
        self.process.sendcontrol('u')


class TestInvocation:

    def test_simple(self):
        assert 1 == 1

    def test_bash(self):
        bash = BashSession()
        import pdb; pdb.set_trace()
