#
# Build bash from source
#

FROM debian:10-slim AS builder

RUN \
    apt-get update && \
    apt-get install -y \
        autoconf \
        autotools-dev \
        bison \
        curl \
        gcc \
        gettext \
        libncurses5-dev \
        make \
        && \
    apt-get clean

ENV BASH_SRC_VERSION 3.2.57
ENV BASH_SRC_SHA256  3fa9daf85ebf35068f090ce51283ddeeb3c75eb5bc70b1a4a7cb05868bfe06a4
ENV BASH_SRC_URL     http://ftpmirror.gnu.org/bash/bash-${BASH_SRC_VERSION}.tar.gz
RUN \
    mkdir /bash-build && \
    cd /bash-build && \
    curl -L "$BASH_SRC_URL" -o bash-source.tar.gz && \
    echo "$BASH_SRC_SHA256 *bash-source.tar.gz" | sha256sum --check - && \
    tar axf bash-source.tar.gz && \
    cd "bash-$BASH_SRC_VERSION"* && \
    ./configure --prefix=/bash && \
    make && \
    make install


#
# Compose environment for automated tests
#

FROM debian:10-slim

RUN \
    apt-get update && \
    apt-get install -y \
        make \
        curl \
        python3 \
        python3-venv \
        bash \
        sed \
        && \
    apt-get clean
COPY --from=builder /bash /bash
ENV PATH /bash/bin:${PATH}
