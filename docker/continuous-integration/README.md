# Setup Jenkins server for automated systems testing with CI/CD pipeline

### Core concept of the QA automation server
![automation server concept](automation-server-concept.png)

### Spin up Jenkins automation server
Install Docker and Docker Compose on the server, then navigate to the [docker/continuous-integration/](https://github.com/CUAHSI/QA-AutomationEngine/blob/develop/docker/continuous-integration/) folder and run:
```
docker network create cuahsi_ci
docker-compose up -d
```
This will create a network interface for the Jenkins container and the SeleniumGrid containers to share.  If the SeleniumGrid is ran on a different host, the network setup step here does not provide any value, but it shouldn't cause problems.  The Jenkins server is then created with the Docker Compose command.
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
This creates Docker containers to simulate users for testing.  The resulting SeleniumGrid system can be used for the testing of any product - the users don't have logins, special configurations, or any other relationship to a specific product.  It's also worth noting that these simulated user containers persist through test suite runs.  However, the system automatically clears cache, cookies, etc. between test executions.