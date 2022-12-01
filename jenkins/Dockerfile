FROM jenkins/jenkins:lts

USER root

RUN apt update && apt install -y docker.io python3 python3-pip
RUN pip3 install docker python-dotenv

COPY ./apidocker-deploy.py /usr/local/sbin/apidocker-deploy.py

RUN chmod +x /usr/local/sbin/apidocker-deploy.py
RUN echo '{\n    "registry-mirrors": [],\n    "insecure-registries":["registry.domain.com"],\n    "dns": ["8.8.8.8"],\n    "debug": false,\n    "experimental": false\n}' > /etc/docker/daemon.json

USER jenkins
