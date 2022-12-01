#!/usr/bin/python3
# -*- coding: utf-8 -*-

import docker
import os
import sys
import time
from dotenv import load_dotenv

### #####################################################################
### Versão Mínima do Python

assert sys.version_info >= (3, 6)


### #####################################################################
### Diretório de execução do script

BASEDIR = os.getcwd()
FILE_DOTENV = os.path.join(BASEDIR, '.env')

load_dotenv(FILE_DOTENV)


### #####################################################################
### Variaveis de Ambiente

DOCKER_TYPE = os.getenv("DOCKER_TYPE")
DOCKER_API_SERVER = os.getenv("DOCKER_API_SERVER")
DOCKER_API_PORT = os.getenv("DOCKER_API_PORT")

REGISTRY = os.getenv("REGISTRY")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

REPOSITORY = os.getenv("REPOSITORY")
TAG = os.getenv("TAG")


ENVS = {}
_ENVS = os.getenv("ENVS")
if _ENVS:
    _ENVS_LIST =  list(filter(None, _ENVS.split(',')))
    for env in _ENVS_LIST:
        VAR = env.split(':')
        ENVS[str(VAR[0])] = str(VAR[1])


LABELS = {}
_LABELS = os.getenv("LABELS")
if _LABELS:
    _LABELS_LIST = list(filter(None, _LABELS.split(',')))
    for env in _LABELS_LIST:
        VAR = env.split(':')
        LABELS[str(VAR[0])] = str(VAR[1])


PORTS = {}
_PORTS = os.getenv("PORTS")
if _PORTS:
    _PORTS_LIST =  list(filter(None, _PORTS.split(',')))
    for port in _PORTS_LIST:
        VAR = port.split(':')
        PORTS[int(VAR[0])] = int(VAR[1])


VOLUMES = []
_VOLUMES = os.getenv("VOLUMES")
if _VOLUMES:
    VOLUMES = list(filter(None, _VOLUMES.split(',')))


EXTRAHOSTS = {}
_EXTRAHOSTS = os.getenv("EXTRA_HOSTS")
if _EXTRAHOSTS:
    _EXTRAHOSTS_LIST =  list(filter(None, _EXTRAHOSTS.split(',')))
    for port in _EXTRAHOSTS_LIST:
        VAR = port.split(':')
        EXTRAHOSTS[str(VAR[0])] = str(VAR[1])


if not DOCKER_TYPE:
    BASE_URL = 'unix://var/run/docker.sock'
elif DOCKER_TYPE.upper() == "UNIX":
    BASE_URL = 'unix://var/run/docker.sock'
else:
    BASE_URL = 'tcp://{0}:{1}'.format(DOCKER_API_SERVER, DOCKER_API_PORT)


### #####################################################################
### Conector Local da API

client_docker = docker.DockerClient(base_url = BASE_URL)


### #####################################################################
### Procedimentos Funções

def print_no_line(TEXT):
    sys.stdout.write(TEXT)
    sys.stdout.flush()


def list_container_running(client):
    CONTAINER_RUN = []
    for container in client.containers.list():
        CONTAINER_RUN.append(container.name)
    return CONTAINER_RUN


def login_registry(client, _registy, _username, _password):
    login = client.login(
        registry = _registy,
        username = _username,
        password = _password)
    return login


def pull_image(client, registry, repository, tag):
    image = client.images.pull(repository='{0}/{1}'.format(registry, repository), tag=tag, decode=True)
    #image_sha256 = image.id
    return image


def container_run(client, registry, repository, tag, ports, volumes, envs, extrahosts, labels):
    for check_container in client_docker.containers.list(all=True):
        if REPOSITORY in check_container.name:
            STATUS = check_container.status
            if STATUS == 'running':
                check_container.stop()
                print_no_line('stopped ')
                check_container.remove()
                print_no_line('removed ')
            elif STATUS == 'exited' or STATUS == 'stopped' or STATUS == 'created':
                check_container.remove()
                print_no_line('removed ')

    container = client_docker.containers.run(
            image = '{0}/{1}:{2}'.format(registry, repository, tag),
            name = repository,
            ports = ports,
            environment = envs,
            volumes = volumes,
            labels = labels,
            extra_hosts = extrahosts,
            restart_policy = {'Name': 'always'},
            detach=True)
    for container in client_docker.containers.list(all=True):
        if REPOSITORY in container.name:
            STATUS = False
            while STATUS == False:
                if container.status == 'created':
                    print_no_line('.')
                    time.sleep(3)
                elif container.status == 'running':
                    print_no_line('running ')
                    STATUS = True
    


### #####################################################################
### Inicial Script

print('Status: Client = {0}'.format(BASE_URL))

### Login Registry
print_no_line('Status: ')
login = login_registry(client_docker, REGISTRY, USERNAME, PASSWORD)
print(login.get('Status'))

### Pull Image
print_no_line('Status: ')
image = pull_image(client_docker, REGISTRY, REPOSITORY, TAG)
print(image)

### Start/Restart Image
print_no_line('Status: ')
container_run(client_docker, REGISTRY, REPOSITORY, TAG, PORTS, VOLUMES, ENVS, EXTRAHOSTS, LABELS)
print()

sys.exit(0)
