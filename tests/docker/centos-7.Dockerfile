FROM centos:7

RUN yum -y --setopt=tsflags=nodocs update && \
    yum -y --setopt=tsflags=nodocs install \
        make \
        curl \
        python3 \
        bash \
        sed \
        && \
    yum clean all
