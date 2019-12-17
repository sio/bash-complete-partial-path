'''
Test keyboard shortcuts
'''


class TestShortcuts:

    def test_tab_cycles(self, bash):
        '''Repeated Tab presses should loop though available completions'''
        command = 'ls u/s/a'
        cycle_length = len(bash.complete(command)) + 1
        completions = {n: bash.complete(command, tabs=n) for n in range(1, cycle_length)}
        for tabs, completion in completions.items():
            next_cycle = bash.complete(command, tabs=tabs + cycle_length)
            assert completion == next_cycle, 'tabs: {}, old: {}, new: {}'.format(
                                                tabs, completion.selected, next_cycle.selected)

