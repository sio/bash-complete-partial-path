'''
Test enhanced completion for paths with special chars
'''

from pathlib import Path
import pytest


class TestSpecialCharacters:
    '''All subtests will use the same bash session'''

    @pytest.mark.parametrize(
        'special,shortcut',
        [
            ('usr/share/a file with spaces', 'u/s/a'),
            ('some/very/weird &file!', 's/v/w'),
        ]
    )
    @pytest.mark.parametrize('quotes', ['', '"', "'"])
    def test_special_chars(self, bash, special, shortcut, quotes):
        '''Test special character handling'''
        special_path = Path(bash.tmpdir) / special
        parent = special_path.parents[0]
        if not parent.exists():
            parent.mkdir(parents=True)  # exist_ok is not supported in Python 3.4
        special_path.touch()

        command = 'ls {}{}'.format(quotes, shortcut)
        output = bash.complete(command)

        if len(output) == 1:
            assert quotes + special in output.selected
        if quotes:  # shlex fails when completion happens in open quotes
            output = str(output)
        assert special in output
