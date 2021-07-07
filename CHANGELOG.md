# Release history for bash-complete-partial-path

## v1.1.0-dev (unreleased)

Development version. Work is being done on adding support for bash 3.2 (issue #8)


## v1.0.0 (2019-12-04)

The project has been around for a long time, but no formal releases were
made. From now on the project will follow semantic versioning convention.

Current release of bash-complete-partial-path is considered stable and all users
are recommended to upgrade to this version.

All desired functionality is implemented and has been in use for more than a
year on several platforms. Automated tests and CI were added recently to
detect regressions and to monitor compatibility with all supported platforms.

Changes introduced over the past year:

- Fixed behavior mismatch with default completion when completing simple paths
  (#10)
- Fixed compatibility issues with older bash (4.2) and sed (4.2.2) - still in
  use in RedHat Linux 7.7
- Ignore any aliases set up by user when calling core system commands


## Untagged release (2018-09-20)

A lot of development happened in the first months:

- Sourcing the completion script is now free of side effects. All
  configuration happens via explicit calls to `_bcpp` manager function
- macOS is now supported
- Shift+Tab can now be used to go back through completion variants
- Environment variables are correctly expanded
- Rare occurences of garbage output are fixed


## Untagged release (2018-07-15)

First published version of bash-complete-partial-path was able to correctly
complete partial paths, non-Linux systems were not yet supported though.
