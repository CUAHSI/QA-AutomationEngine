# Setup Jenkins server for automated systems testing with CI/CD pipeline

### Core concept of the QA automation server
![automation server concept](automation-server-concept.png)

### Spin up Jenkins automation server
Install Docker and Docker Compose on the server, then navigate to the [docker/continuous-integration/](https://github.com/CUAHSI/QA-AutomationEngine/blob/develop/docker/continuous-integration/) folder and run:
```
docker-compose up -d
```
### Install system through GUI on port 8080.
* ``` docker exec -it [DOCKER CONTAINER NAME] cat /var/jenkins_home/secrets/initialAdminPassword ``` to get the instance password
* Install suggested plugins
* Use "Continue as admin" instead of creating a user
### Setup the "command core" and "hydroshare-job-template" jobs
```
docker exec -t [DOCKER CONTAINER NAME] bash /var/jenkins_home/cuahsi/jenkins/setup.sh
```
### Spin up simulated users
Navigate to the [docker/continuous-integration/](https://github.com/CUAHSI/QA-AutomationEngine/blob/develop/docker/continuous-integration/) folder and run:
```
bash simulate-users.sh
```