'''
Interactive debugging in test environment
'''
import os
import pytest


@pytest.mark.skipif('BCPP_TEST_DEBUG' not in os.environ, reason='skipping interactive pdb session')
def test_debug(bash):
    import pdb; pdb.set_trace()
