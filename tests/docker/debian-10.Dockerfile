FROM debian:10-slim

RUN \
    apt-get update && \
    apt-get install -y \
        make \
        python3 \
        python3-venv \
        bash \
        sed \
        && \
    apt-get clean
