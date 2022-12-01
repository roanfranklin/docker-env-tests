## dcoker-env-tests

Um ambiente de teste para estudos DevOps, treinamentos e até para uso de desenvolvimento.

**OBS.:** É preciso saber um pouco mais de Docker para usar o Docker Remote API, assim como configurar o Traefik corretamente e ter que escrever um script para comunicação com as máquinas docker na rede local.

**OBS. IMPORTANTE:** Este ambiente não possui escalabilidade nem disponibilidade em caso de falha num serviço X, pode parar todo o ambiente.



Servidor/Serviços Principal:

- Traefik
- Nexus
- Gogs
- Jenkins
- Portainer*
- SonarQube*

* Pode realizar o procedimento sem essas ferramentas. O Portainer é para gerenciar mais fácil o Docker localmente e até os remotos em um único local. O SonarQube é um analisador de vulnerabilidade que inicialmente pode não ser utilizado, mas a sua função em um contexto geral é muito importante.



Servidor/Serviços SGDB 1 e 2:

- MySQL
- PostgreSQL

**OBS.:** Estão separados, mas podem estar em um mesmo Servidor;



Servidor/Serviços Aplicações:

- Python
- NodeJS
- PHP
- Ruby
- dotNET
- Java
- outros



---
### Requisitos:

- docker
- docker-compose



---
### Configurações Iniciais:

**1º** Realizar a criação do Network e Volumes no docker:

- Network
```bash
docker network create mynet
```

- Volumes
```bash
docker volume create gogs_data
docker volume create gogs_backup
docker volume create gogs_db

docker volume create jenkins_home

docker volume create nexus_data

docker volume create portainer_data

docker volume create sonarqube_data
docker volume create sonarqube_extensions
docker volume create sonarqube_logs
docker volume create sonarqube_db
docker volume create sonarqube_db_data

docker volume create traefik_letsencrypt
docker volume create traefik_certs
docker volume create traefik_logs
```


**2º** Para que você consiga Logar/Pull/Push no registry, deve-se criar/configurar o arquivo */etc/docker/daemon.json*

```json
{
 "registry-mirrors": [],
 "insecure-registries":["registry.domain.com"],
 "dns": ["8.8.8.8"],
 "debug": false,
 "experimental": false
}
```

**OBS.:** Realizar um restart no serviço Docker.

```bash
systemctl restart docker
```


**3º** Configuração do acesso por nome (DNS):

Para funcionar quase 100% em sua rede, é preciso configurar o DNS local da sua maquina para poder acessar o *SERVICO.domain.com*

- Descubra qual o IP da máquina a qual está rodando o docker e os serviços para montar igual a linha abaixo e adicione ao */etc/hosts* no Linux ou outros SO com base Unix. No Linux fica em *C:/Windows/System32/drivers/etc/hosts*.

```
192.168.0.253 traefik.domain.com portainer.domain.com nexus.domain.com registry.domain.com git.domain.com jenkins.domain.com sonar.domain.com
```

OBS.: Qualquer aplicação/apontamento a mais que você construir, deve-se adicionar a lista!



---
### Containers:

O primeiro container que você deve ativar é o Traefik, depois é só ir ativando os demais.

**OBS.:** Informação importante é que estão configurados com domínio locais e o certificado não será válido.



**Traefik:** O usuário e senha setado no Traefik foi gerado pelo comando docker abaixo, usando a imagem httpd:

```bash
docker run --entrypoint htpasswd httpd:2 -Bbn USUARIO SENHA
```

**OBS.:** A senha criada contem o caracter ``$`` e ao setar diretamente no docker-compose.yml, deve-se duplicar, ficando ``$$``



**Nexus / Registry:** O Nexus contém 2 (duas) portas, pois deve-se realizar a configuração de registry docker (hosted) para a segunda porta (8082).