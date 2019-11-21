'''
Shared fixtures for completion testing
'''

from pathlib import Path
from tempfile import TemporaryDirectory
import pytest

from tests.common import BashSession
import tests.logging


BCPP = 'bash_completion'  # relative path from repo's top level

STARTUP = [
    'source "{}"'.format(Path(BCPP).resolve()),
    '_bcpp --defaults',
]
FILETREE = {
    'files': [
        'usr/somefile',
        'usr/share/afile',
    ],
    'dirs': [
        'usr/share/applications',
        'usr/share/another',
        'usr/share/anything',
    ],
}


@pytest.fixture(scope='class')
def bash(log) -> BashSession:
    '''
    Fixture for automated tests.

    Provides BashSession object initialized in a temporary directory with bcpp
    preloaded. Temp directory is cleaned up automatically
    '''
    with TemporaryDirectory(prefix='bcpp_test_') as tmpdir:
        log.debug('Creating bash fixture: %s', tmpdir)
        shell = BashSession(
            startup=STARTUP,
            cwd=tmpdir,
        )
        shell.tmpdir = tmpdir

        root = Path(tmpdir)
        for dirname in FILETREE['dirs']:
            (root / dirname).mkdir(parents=True)
        for filename in FILETREE['files']:
            (root / filename).touch()

        yield shell
        log.debug('Destroying bash fixture: %s', tmpdir)


@pytest.fixture(scope='session')
def log():
    return tests.logging.setup()
