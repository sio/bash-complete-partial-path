'''
Reusable base objects for automating bash interaction
'''

import os
import platform
import re
from itertools import chain

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
    STARTUP = [
        "bind 'set bell-style none'",
    ]
    ENV_UNSET = [
        # The following variables will be unset in test environment
    ]
    ENV_FORCE = {
        # The following variables will be force overwritten with these values
        'PS1': '__>>>__',
        'TERM': 'dumb',
        'HISTFILE': '/dev/null',  # Do not write history for test sessions
    }
    MARKER = '>>-!-<<'
    COLOR_CODE = re.compile('\x1b' r'\[(?:(?:\d{0,3};?){1,4}m|K)')

    def __init__(self, *a,
                 cmd='bash',
                 args='--norc --noprofile',
                 env=None,
                 startup=None,
                 **ka):
        if a:
            raise ValueError('only keyword arguments are supported')
        self.PS1 = self.ENV_FORCE['PS1']

        environment = os.environ.copy()
        for variable in self.ENV_UNSET:
            environment.pop(variable, None)
        if env:
            environment.update(env)
        environment.update(self.ENV_FORCE)

        self.process = pexpect.spawn(
            '{} {}'.format(cmd, args),
            env=environment,
            encoding=self.ENCODING,
            dimensions=(24, 160),  # https://github.com/scop/bash-completion/blob/fb46fed657d6b6575974b2fd5a9b6529ed2472b7/test/t/conftest.py#L112-L115
            **ka
        )
        for command in chain(self.STARTUP, startup or ()):
            self.execute(command)

    def complete(self, text, tabs=1, drop_colors=True):
        '''
        Trigger completion after inputting text into interactive bash session

        Return completion results
        '''
        self._clear_current_line()

        proc = self.process
        proc.send('{}{}'.format(text, '\t' * tabs))
        proc.expect_exact(text)
        proc.send(self.MARKER)
        match = proc.expect([re.escape(self.MARKER), self.PS1])
        if match == 1 and proc.before and not proc.before.strip('\r'):  # drop \r\rPS1
            proc.expect([re.escape(self.MARKER), self.PS1])
        output = proc.before.strip()

        backspaces = 0
        for char in output:
            if char == '\x08':
                backspaces += 1
            else:
                break
        if backspaces:  # handle BACKSPACE characters in the beginning of completion
            output = text[:-backspaces] + output[backspaces:]

        if drop_colors:
            output = self._clean_color_codes(output)

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

    def _clean_color_codes(self, text):
        '''Remove escape sequences for color codes from text'''
        return self.COLOR_CODE.sub('', text)
