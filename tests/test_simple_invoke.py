import platform
import pytest


if platform.system() == 'Windows':  # ptys are not available in Windows
    import pexpect.popen_spawn
    spawn = pexpect.popen_spawn.PopenSpawn  # does not work, bash detects it and behaves differently
else:
    import pexpect
    spawn = pexpect.spawn


class CompletionTestSuite:
    BASH_CMD = 'bash --norc --noprofile'

    def bash(self):
        shell = spawn(self.BASH_CMD)
        return shell


class TestInvocation(CompletionTestSuite):

    def test_simple(self):
        assert 1 == 1

    def test_bash(self):
        import pdb; pdb.set_trace()
