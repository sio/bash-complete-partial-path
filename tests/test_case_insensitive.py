import pytest

@pytest.mark.parametrize('path', ['u/s/a','us/s'])
def test_case_insensitive(bash, path):
    '''Test case insensitive path expansion'''
    ls = 'ls %s'
    assert bash.complete(ls % path) == bash.complete(ls % path.upper())
