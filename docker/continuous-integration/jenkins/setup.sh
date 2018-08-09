INITPASS=$(cat /var/jenkins_home/secrets/initialAdminPassword) \
&& CRUMB=$(curl -k -s "http://localhost:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)" --user "admin":"$INITPASS") \
&& curl -s -X POST "http://localhost:8080/createItem?name=command-core" -k -H "$CRUMB" --user "admin":"$INITPASS" --data-binary "@jobs/command-core.xml" -H "Content-Type:text/xml"
