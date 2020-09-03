# Automated tests for bash-complete-partial-path

## Running tests

Execute `make test` from repo's top directory


## Dependencies

Test environment needs to provide:

- Python 3.4+
- GNU Make
- Curl
- sha256sum (from GNU Coreutils)

_* curl and sha256sum may be avoided if you fetch Makefile.venv manually_

And all of bash-complete-partial-path dependencies:

- GNU Bash
- GNU Sed


## Tests implementation

Automated tests are implemented in Python and make use of [pytest] and [pexpect].
Makefile provided with the test suite takes care of managing virtual
environment for Python automatically, no system-wide changes to Python
installation are made.

Because of unconventional command line implementation automated tests can not
be executed on Windows. Thanks to recent developments ([ConPty]) that may
become possible in the future - if/when Windows will be fully supported by
pexpect.

[pytest]: https://docs.pytest.org/en/stable/
[pexpect]: https://pexpect.readthedocs.io/en/stable/
[ConPTY]: https://devblogs.microsoft.com/commandline/windows-command-line-introducing-the-windows-pseudo-console-conpty/


## CI setup

Automated tests are continuously executed after each push to this repo.

- **Linux** tests are executed within [Docker containers] on the
  infrastructure provided by [GitHub Actions]. The following configurations are
  being tested:
    - Centos 7: bash 4.2, sed 4.2
    - Debian 8: bash 4.3, sed 4.2
    - Debian 9: bash 4.4, sed 4.4
    - Debian 10: bash 5.0, sed 4.7
    - Debian 11: bash 5.0, sed 4.7 *(Debian 11 is the testing branch of
      Debian, package versions are not frozen and may be updated)*
- **macOS** tests are executed in [virtual environment] provided by [Cirrus CI]:
    - macOS 10.15: bash 5.0, sed 4.8 *(these numbers will change - packages
      are automatically updated to the latest version in each CI run)*
- **FreeBSD** tests are executed in Google Cloud Platfom [VM images] on
  infrastructure provided by [Cirrus CI]:
    - FreeBSD 12.1: bash 5.0, sed 4.7 *(automatically updated in each CI run)*

[GitHub Actions]: https://github.com/features/actions
[Docker containers]: docker/README.md
[virtual environment]: https://cirrus-ci.org/guide/macOS/
[VM images]: https://cirrus-ci.org/guide/FreeBSD/
[Cirrus CI]: https://cirrus-ci.org/


## Test configuration

### Modifying test runner behavior

The following environment variables affect behavior of test runner:

- **BCPP_TEST_DEBUG** -
  If this variable is set, PDB session will be activated by one of the test
  cases. Standard `bash` fixture will be available in that session.
- **BCPP_TEST_LOG_FILE** -
  Path to the file where test debug messages will be saved.
- **BCPP_TEST_LOG_STDOUT** -
  Print test debug messages to stdout. Pytest shows stdout only for failed
  tests by default, see [documentation](https://docs.pytest.org/en/latest/capture.html).
- **BCPP_TEST_PEXPECT_TIMEOUT** -
  Timeout in seconds for Pexpect to wait for terminal output. Increase this
  value if test runner is a slow or overloaded machine.
- **BCPP_TEST_SCOP_COMPLETION** -
  Path to scop/bash-completion script for compatibility testing. If this
  variable is not set the corresponding tests will be skipped.

Check if the list above is up to date:

```
$ git grep -woEh 'BCPP\w+' tests/|sort -u
```

### Passing extra arguments to pytest

Use **PYTEST_ADDOPTS**
([documentation](http://doc.pytest.org/en/latest/customize.html#adding-default-options)):

- Stopping after the first failure: `make test PYTEST_ADDOPTS=-x`
- Running specific test: `make test PYTEST_ADDOPTS='-k test_case_or_suite_name'`
- Dropping into PDB on failures: `make test PYTEST_ADDOPTS=--pdb`
    - While in PDB you may interact with bash session via
      `bash.process.interact()`. Press `Ctrl+]` to detach from bash session
      and return to PDB.
- Other examples:

```
$ make test PYTEST_ADDOPTS=-x
$ make test PYTEST_ADDOPTS=-xv
$ make test PYTEST_ADDOPTS='-xv -k TestShortcuts'
$ make test PYTEST_ADDOPTS='-xvv -k test_case'
$ make test PYTEST_ADDOPTS='-xvv -k test_env_clean'
$ make test PYTEST_ADDOPTS='-xvv -k test_env_clean --pdb'
```
