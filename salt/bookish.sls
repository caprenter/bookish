docker-installed:
    pkg.installed:
        - name: docker.io

docker-running:
    service.running:
        {% if grains['lsb_distrib_release']=='14.04' %}
        - name: docker.io
        {% else %}
        - name: docker
        {% endif %}

docker-py:
  pkg.installed:
    - name: python-pip
  pip.installed:
    - name: docker_py>=0.5,<0.6

# https://github.com/saltstack/salt/issues/15803

bjwebb/bookish:
    docker.pulled:
      - tag: latest-demo
      - require:
        - pip: docker-py

docker_bookishdemo_stop_if_old:
  cmd.run:
    - name: docker stop bookishdemo
    - unless: docker inspect --format "\{\{ .Image \}\}" bookishdemo | grep $(docker images | grep "bjwebb/bookish:latest-demo" | awk '{ print $3 }')
    - require:
      - docker: bjwebb/bookish

docker_bookishdemo_remove_if_old:
  cmd.run:
    - name: docker rm bookishdemo
    - unless: docker inspect --format "\{\{ .Image \}\}" bookishdemo | grep $(docker images | grep "bjwebb/bookish:latest-demo" | awk '{ print $3 }')
    - require:
      - cmd: docker_bookishdemo_stop_if_old

bookishdemo-container:
  docker.installed:
    - name: bookishdemo
    - image: bjwebb/bookish:latest-demo
    - environment:
      - SECRET_KEY: 'c9a7789b3e18f89c93efcbbb3072671bfa7b1d02474b5d02c747ffc9a8146768'
      - DATABASE_URL: 'sqlite:///demo.db'
      - DEBUG: 'True'
    - require:
      - cmd: docker_bookishdemo_remove_if_old

bookishdemo-service:
  docker.running:
    - container: bookishdemo
    - port_bindings:
        '8000/tcp':
            HostIp: ''
            HostPort: '80'
    - require:
      - docker: bookishdemo-container

