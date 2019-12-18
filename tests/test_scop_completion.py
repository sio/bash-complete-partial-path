import os
import pytest

from tests.conftest import STARTUP


ENV_SCOP = 'BCPP_TEST_SCOP_COMPLETION'


@pytest.mark.skipif(ENV_SCOP not in os.environ, reason='environment variable not set: %s' % ENV_SCOP)
def test_scop_completion(bash):
    '''Test compatibility with main bash-completion package'''
    bash.execute('exec bash --norc --noprofile')

    declare = bash.execute('declare -F')
    assert '_filedir' not in declare
    assert '_bcpp_filedir' not in declare

    bash.execute('source "${}"'.format(ENV_SCOP))
    for cmd in STARTUP:
        bash.execute(cmd)

    declare = bash.execute('declare -F')
    assert '_filedir' in declare
    assert '_bcpp_filedir' in declare

    completion = bash.complete('ls u/s/a')
    assert len(completion) > 1
    assert 'usr/share/applications' in completion
