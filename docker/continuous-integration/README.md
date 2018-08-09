# Setup Jenkins server for automated systems testing with CI/CD pipeline

1. Spin up Jenkins automation server `docker-compose up -d`
1. Install system through GUI on port 8080.
   Use "Continue as admin" instead of creating a user
   Install suggested plugins
1. Setup the "command core" job
```bash
docker exec -t [DOCKER CONTAINER NAME] bash /var/jenkins_home/cuahsi/jenkins/setup.sh
```
