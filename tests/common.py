'''
Reusable base objects for automating bash interaction
'''

import os
import platform
import re
import shlex
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
        "bind 'set enable-bracketed-paste off'",
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
    TIMEOUT = os.getenv('BCPP_TEST_PEXPECT_TIMEOUT', 60)

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

    def complete(self, text, tabs=1, custom_tabs='', drop_colors=True):
        '''
        Trigger completion after inputting text into interactive bash session

        Return completion results
        '''
        self._clear_current_line()

        proc = self.process
        proc.send('{}{}'.format(text, custom_tabs or '\t' * tabs))
        proc.expect_exact(text, timeout=self.TIMEOUT)
        proc.send(self.MARKER)
        match = proc.expect(re.escape(self.MARKER), timeout=self.TIMEOUT)
        output = proc.before.strip()
        proc.sendcontrol('c')  # drop current input
        proc.expect_exact(self.PS1, timeout=self.TIMEOUT)
        return CompletionResult(command=text, output=output, prompt=self.PS1, drop_colors=drop_colors)

    def execute(self, command, timeout=-1, exitcode=0):
        '''
        Execute a single command in interactive shell. Check its return code.

        Return terminal output after execution.
        '''
        if timeout == -1:
            timeout = self.TIMEOUT

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
        if not returned:
            returned = '0'  # macOS allows empty exit codes apparently:
                            # https://github.com/sio/bash-complete-partial-path/runs/354401396
        if str(exitcode) != returned:
            message = '{command} exited with code {returned} (expected {exitcode})\n{output}'
            raise BashSessionError(message.format(**locals()))

        return output

    def _clear_current_line(self):
        '''Clear any input on the current line <https://askubuntu.com/a/471023>'''
        self.process.sendcontrol('e')
        self.process.sendcontrol('u')


class CompletionResult:
    COLOR_CODE = re.compile('\x1b' r'\[(?:(?:\d{0,3};?){1,4}m|K)')
    BACKSPACE = '\x08'

    def __init__(self, command, output, prompt, drop_colors=True):
        '''Parse completion results from raw completion output'''
        output = output.strip()

        # Clean up backspace characters
        cleaned = []
        for position, char in enumerate(output):
            if char == self.BACKSPACE:
                if position == 0:
                    cleaned = list(command)
                cleaned.pop()
            else:
                cleaned.append(char)
        output = ''.join(cleaned)

        # Clean up \r\rPS1
        output = re.sub(r'^\r+%s' % prompt, '', output)

        # Clean up color codes
        if drop_colors:
            output = self._clean_color_codes(output)

        # Parse output
        if prompt in output:
            variants, selected = (x.strip() for x in output.split(prompt))
        else:
            variants = selected = output.strip()
        self._variants = variants
        self.selected = selected

    @property
    def variants(self):
        '''Split variant according to shell lexical rules'''
        return shlex.split(self._variants) if self._variants else [self.selected]

    def __contains__(self, item):
        return item in self.variants

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        elif isinstance(other, type(self)):
            return (self._variants == other._variants and
                    self.selected == other.selected)
        else:
            return NotImplemented

    def __bool__(self):
        return bool(self.selected) or bool(self._variants)

    def __iter__(self):
        yield from self.variants

    def __repr__(self):
        return '<{cls} selected={selected!r}, variants={variants!r}>'.format(
            cls=self.__class__.__name__,
            selected=self.selected,
            variants=self.variants,
        )

    def __str__(self):
        return self._variants or self.selected

    def __len__(self):
        return len(self.variants)

    def _clean_color_codes(self, text):
        '''Remove escape sequences for color codes from text'''
        return self.COLOR_CODE.sub('', text)
