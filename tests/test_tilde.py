'''
Tests for tilde expansion
https://www.gnu.org/software/bash/manual/html_node/Tilde-Expansion.html
'''


from getpass import getuser
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest


@pytest.mark.parametrize('tilde', ['~', '~{}'.format(getuser())])
def test_home(bash, tilde):
    '''~, ~username expansion'''
    home = Path.home()
    subdir = Path('foo/bar/baz')
    with TemporaryDirectory(prefix='.bcpp-test-', dir=str(home)) as tmpdir:
        testdir = home / tmpdir / subdir
        testdir.mkdir(parents=True)
        assert testdir.exists()
        command = 'ls {}/{}/f/b/b'.format(tilde, Path(tmpdir).relative_to(home))
        completed = bash.complete(command)
        assert completed, 'no completion for: %s' % command
        assert completed == 'ls {}'.format(testdir)


def test_pushd(bash):
    '''~1, ~2 expansion'''
    bash.execute('pushd usr')
    directory = Path('usr/share/applications')
    assert bash.complete('ls ~1/u/s/app') == 'ls {}'.format(bash.tmpdir / directory)
