FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3.8 && \
    if [ ! -e /usr/bin/pip ]; then ln -s /usr/bin/python3.8 /usr/bin/python3; fi && \
    apt-get install -y python3-pip

ADD ./ /home/work/projects
ADD start.sh /
RUN chmod +x /start.sh && pip3 install -r /home/work/projects/requirements.txt && rm -rf ~/.cache/pip

CMD ["/start.sh"]
