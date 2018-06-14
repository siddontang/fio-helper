FROM centos:7

RUN yum update -y \
    && yum install -y fio \
    && yum clean all

RUN mkdir /fio

ADD . /fio

VOLUME /fio