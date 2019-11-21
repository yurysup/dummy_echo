FROM centos:latest
RUN yum install -y nc

COPY ./boot.sh /
RUN chmod +x /boot.sh
ENTRYPOINT ["/boot.sh"]

EXPOSE 5000
