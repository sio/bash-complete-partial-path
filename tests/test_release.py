'''
Sanity checks for new release
'''

from shutil import which
from subprocess import Popen, PIPE
import re

import pytest


BCPP = 'bash_completion'
CHANGELOG = 'CHANGELOG.md'
VERSION = re.compile(r'\b(v\d+\.\d+\.\d(?:-[\w\d]+|\b))')  # semver


skipif_no_git = pytest.mark.skipif(not which('git'), reason='git not found in $PATH')


def skip_development_versions(message=None):
    '''Skip some tests on development versions'''
    app_version = read_version(BCPP, lines=5)
    if app_version.endswith('-dev'):
        pytest.skip(message or 'skip checks for -dev versions')


def run(command, **ka):
    '''Backwards compatible subprocess runner'''
    process = Popen(command, **ka)
    exit_code = process.wait()
    output = process.stdout.read().decode().strip()
    if exit_code:
        raise RuntimeError('command returned {}: {}'.format(exit_code, ' '.join(command)))
    return output


def read_version(filename, lines=None):
    '''Read version from first lines of file'''
    with open(filename) as f:
        for num, line in enumerate(f):
            if lines and num == lines:
                break
            match = VERSION.search(line)
            if match:
                return match.group(1)
        else:
            raise ValueError('version pattern not found in {}'.format(filename))


def read_git_ref(name):
    '''Dereference git commit ID'''
    command = 'git show-ref -s --heads --tags'.split() + [name]
    return run(command, stdout=PIPE)


def test_readme_changelog():
    '''Compare version numbers in main script and CHANGELOG'''
    app_version = read_version(BCPP, lines=5)
    changelog_version = read_version(CHANGELOG, lines=5)
    assert app_version == changelog_version


@skipif_no_git
def test_git_tag():
    '''Compare version numbers in main script and git tag'''
    skip_development_versions()
    app_version = read_version(BCPP, lines=5)
    command = 'git log -1 --format=%D --'.split() + [BCPP]
    output = run(command, stdout=PIPE)
    match = VERSION.search(output)
    if not match:
        raise AssertionError('version pattern not found in {}'.format(' '.join(command)))
    git_version = match.group(1)
    assert app_version == git_version


@skipif_no_git
def test_git_stable():
    '''Check that git stable tag points to the latest CHANGELOG entry'''
    skip_development_versions()
    stable = read_git_ref('stable')
    changelog = read_git_ref(read_version(CHANGELOG, lines=5))
    assert stable == changelog
