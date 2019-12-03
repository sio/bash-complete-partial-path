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
  infrastructure provided by [CircleCI]. The following configurations are
  being tested:
    - Debian 8: bash 4.3, sed 4.2
    - Debian 9: bash 4.4, sed 4.4
    - Debian 10: bash 5.0, sed 4.7
    - Debian 11: bash 5.0, sed 4.7 *(Debian 11 is the testing branch of
      Debian, package versions are not frozen and may be updated)*
- **macOS** tests are executed in [virtual environment] provided by [GitHub
  Actions]:
    - macOS 10.15: bash 5.0, sed 4.7 *(these numbers will change - packages
      are automatically updated to the latest version in each CI run)*

[CircleCI]: https://circleci.com/
[GitHub Actions]: https://github.com/features/actions
[Docker containers]: docker/README.md
[virtual environment]: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/software-installed-on-github-hosted-runners#macos-1015
