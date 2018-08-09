# Setup Jenkins server for automated systems testing with CI/CD pipeline

### Spin up Jenkins automation server
```
docker-compose up -d
```
### Install system through GUI on port 8080.
* Use "Continue as admin" instead of creating a user
* Install suggested plugins
### Setup the "command core" job
```
docker exec -t [DOCKER CONTAINER NAME] bash /var/jenkins_home/cuahsi/jenkins/setup.sh
```
