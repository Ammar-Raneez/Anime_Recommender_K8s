### Run Jenkins with DINS capabilities
```bash
docker run -d --name jenkins-dind --privileged -p 8080:8080 -p 50000:50000 -v //var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home jenkins-dind
```

### View initial Jenkins password
```bash
docker logs jenkins-dind
```

### Install Python and change Python3 call to Python
```bash
docker exec -u root -it jenkins-dind bash
    apt update -y
    apt install -y python3
    python3 --version
    ln -s /usr/bin/python3 /usr/bin/python
    python --version
    apt install -y python3-pip
    apt install -y python3-venv
    exit

docker restart jenkins-dind
```

### Install GCP CLI and K8s
```bash
docker exec -u root -it jenkins-dind bash
    apt-get update
    apt-get install apt-transport-https ca-certificates gnupg curl
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    apt-get update && apt-get install google-cloud-cli
    apt-get update && apt-get install -y kubectl
    apt-get install -y google-cloud-sdk-gke-gcloud-auth-plugin
```

### Grant Docker permission to Jenkins
```bash
docker exec -u root -it jenkins-dind bash
    groupadd docker
    usermod -aG docker jenkins
    usermod -aG root jenkins
    exit
    docker restart jenkins-dind
```
