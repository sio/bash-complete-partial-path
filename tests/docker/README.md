# Environments for bash-complete-partial-path tests

Docker environments for automated testing of [bash-complete-partial-path][bcpp].

- Images are published at GitHub Container Registry: [`ghcr.io/sio/bash-complete-partial-path`][registry]
- Docker tags correspond to [`*.Dockerfile`][dockerfiles] filenames
- Automatic builds are triggered by pushing to `master` or to `dockerhub`
  (if any of Dockerfiles were modified)
- Containers are also rebuilt automatically on a regular schedule

[bcpp]: https://github.com/sio/bash-complete-partial-path
[registry]: https://github.com/users/sio/packages/container/bash-complete-partial-path/versions
[dockerfiles]: https://github.com/sio/bash-complete-partial-path/tree/master/tests/docker
