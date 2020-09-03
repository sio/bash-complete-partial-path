'''
Check that environment stays clean after importing bcpp
'''

import difflib
import re
from tests.common import BashSession
from tests.conftest import STARTUP


def grep(needle, haystack):
    results = []
    query = re.finditer(
        r'^(.*%s.*)$' % re.escape(needle),
        haystack,
        re.MULTILINE
    )
    for match in query:
        results.append(match.group(1))
    return results


def test_env_clean():
    '''
    Compare shell environments before and after invoking bcpp
    '''
    cmd_show_env = r"(declare -p; declare -F)|grep -E '^declare\b'|sort"
    declare = re.compile(r'^declare\b(?:\s+\-\S+)+\s+')
    env_item = re.compile(declare.pattern + r'(\w+)')

    ignore_items = {  # Changes to variables from this set are ignored
        'BASHOPTS',   # - meant to be modified by _bcpp
        'BASH_ARGC',  # - volatile, modified almost always
        'BASH_ARGV',  # - volatile, modified almost always
    }

    bash = BashSession()
    before = bash.execute(cmd_show_env)
    for cmd in STARTUP:
        bash.execute(cmd)
    after = bash.execute(cmd_show_env)

    for line in difflib.Differ().compare(before.splitlines(), after.splitlines()):
        content = line[1:].strip()

        match = env_item.match(content)
        if match:
            item = match.group(1)
        else:
            item = content
        if item in ignore_items \
        or not content:
            continue

        error_msg = ''
        if line.startswith('-'):
            error_msg = 'Item missing from environment:\n{line}'
        if line.startswith('+'):
            if not item.lower().startswith('_bcpp'):
                error_msg = 'Extra item in environment:\n{line}'
        if error_msg:
            error_extra = [
                '',
                'Environment before:\n{}'.format('\n'.join(grep(item, before))),
                'Environment after:\n{}'.format('\n'.join(grep(item, after))),
            ]
            raise AssertionError(error_msg.format(line=line) + '\n'.join(error_extra))
