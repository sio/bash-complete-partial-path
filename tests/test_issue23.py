'''
Edge case for directory names containing whitespace

https://github.com/sio/bash-complete-partial-path/issues/23
'''

import pytest

from pathlib import Path

@pytest.fixture(scope='class')
def custom_bash(bash):
    root = Path(bash.tmpdir)
    dirs = [
        root / "abc" / "def ghi",
        root / "abc" / "djkl",
    ]
    for d in dirs:
        d.mkdir(parents=True)
    yield bash

class TestIssue23:
    def test_happy_path(self, custom_bash):
        want = {'abc/def ghi', 'abc/djkl'}
        got = set(custom_bash.complete('cd abc/d'))
        assert got == want

    def test_tricky_path(self, custom_bash):
        want = {'abc/def ghi', 'abc/djkl'}
        got = set(custom_bash.complete('cd abc/'))
        assert got == want
