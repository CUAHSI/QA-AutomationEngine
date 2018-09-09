INITPASS=$(cat /var/jenkins_home/secrets/initialAdminPassword) \
&& CRUMB=$(curl -k -s "http://localhost:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)" --user "admin":"$INITPASS") \
&& curl -s -X POST "http://localhost:8080/createItem?name=command-core" -k -H "$CRUMB" --user "admin":"$INITPASS" --data-binary "@/var/jenkins_home/cuahsi/jenkins/jobs/command-core.xml" -H "Content-Type:text/xml"
&& CRUMB=$(curl -k -s "http://localhost:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)" --user "admin":"$INITPASS") \
&& curl -s -X POST "http://localhost:8080/createItem?name=hydroshare-job-template" -k -H "$CRUMB" --user "admin":"$INITPASS" --data-binary "@/var/jenkins_home/cuahsi/jenkins/jobs/hydroshare-job-template.xml" -H "Content-Type:text/xml"
