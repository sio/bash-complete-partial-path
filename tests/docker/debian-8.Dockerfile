FROM debian:8-slim

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
