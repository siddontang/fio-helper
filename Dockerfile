FROM centos:7

RUN yum update -y \
    && yum install -y fio libaio-devel \
    && yum clean all

RUN mkdir /fio

ADD . /fio

VOLUME /fio