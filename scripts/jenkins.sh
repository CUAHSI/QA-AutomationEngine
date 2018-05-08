while read TEST; do
    CRUMB=$(curl -k -s "http://$JENKINSIP:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)" --user "$USERNAME":"$USERPASS")
    if curl -s -X GET -k -H "$CRUMB" --user "$USERNAME":"$USERPASS" --output /dev/null --head --fail "http://$JENKINSIP:8080/job/$TESTSUITE-$TEST/lastBuild/api/xml?depth=1&token=$APITOKEN"; then
	echo "$TESTSUITE-$TEST exists.  Starting job."
	sleep 1
	curl -s -X POST "http://$JENKINSIP:8080/job/$TESTSUITE-$TEST/buildWithParameters?delay=0sec&TESTCASE=$TEST&token=$APITOKEN" -k -H "$CRUMB" --user "$USERNAME":"$USERPASS"
    else
	echo "$TESTSUITE-$TEST does not exist.  Creating, then starting job."
	sleep 1
	curl -s -X GET "http://$JENKINSIP:8080/job/$TESTSUITE-job-template/config.xml" --user "$USERNAME":"$USERPASS" -o job-template-config.xml
	sleep 1
	curl -s -X POST "http://$JENKINSIP:8080/createItem?name=$TESTSUITE-$TEST" -k -H "$CRUMB" --user "$USERNAME":"$USERPASS" --data-binary @job-template-config.xml -H "Content-Type:text/xml"
	sleep 1
	curl -s -X POST "http://$JENKINSIP:8080/job/$TESTSUITE-$TEST/buildWithParameters?delay=0sec&TESTCASE=$TEST&token=$APITOKEN" -k -H "$CRUMB" --user "$USERNAME":"$USERPASS"
    fi
    sleep 1
done <"../$TESTSUITE/$TESTSUITE.conf"
