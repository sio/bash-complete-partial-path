'''
Test keyboard shortcuts
'''


from hypothesis import (
    given,
    settings,
    strategies as st,
)

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

    @settings(deadline=1000, max_examples=10)
    @given(forward = st.integers(min_value=1, max_value=15),
           backward = st.integers(min_value=1, max_value=15))
    def test_shift_tab(self, bash, log, forward, backward):
        '''Shift-Tab cycles back'''
        command = 'ls u/s/a'
        cycle_length = len(bash.complete(command)) + 1

        TAB = '\t'
        SHIFT_TAB = '\x1b\x5b\x5a'  # use 'showkey -a' on any Linux machine
                                    # to see ASCII codes corresponding to keypresses

        tabs_forward = TAB * ((forward - backward) % cycle_length)
        if not tabs_forward:  # in case we cycle back to the original command
            tabs_forward = TAB + SHIFT_TAB
        tabs_forward_and_back = TAB * forward + SHIFT_TAB * backward
        log.debug(
            '[%s/%s] tab sequences: forward=%r, forward and back=%r',
            forward,
            backward,
            tabs_forward,
            tabs_forward_and_back
        )
        assert bash.complete(command, custom_tabs=tabs_forward) == \
               bash.complete(command, custom_tabs=tabs_forward_and_back)
