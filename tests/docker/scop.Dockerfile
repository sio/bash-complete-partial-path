# Test environment that provides https://github.com/scop/bash-completion

FROM potyarkin/bcpp:debian-10

RUN \
    apt-get install -y bash-completion && \
    apt-get clean

ENV BCPP_TEST_SCOP_COMPLETION /etc/bash_completion
