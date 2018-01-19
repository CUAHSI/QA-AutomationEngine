i="-1" # i controls which thread to run test on
while read TEST; do
    while true; do
	i=$(($i + 1))
	i=$(($i % 8)) # assumes 8 threads available
	CRUMB=$(curl -k -s "http://$JENKINSIP:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)" --user "$USERNAME":"$USERPASS")
	curl -X GET "http://$JENKINSIP:8080/job/$TESTSUITE-thread$i/lastBuild/api/xml?depth=1&token=$APITOKEN" -k -H "$CRUMB" --user "$USERNAME":"$USERPASS" > thread.json
	THREAD=$(grep -c '<building>false</building>' thread.json)
	if [ "$THREAD" = "1" ]; then
	    echo "Thread $i Available"
	    sleep 1
	    break
	else
	    echo "Thread $i Not Available"
	    sleep 1
	fi
	sleep 1
    done
    CRUMB=$(curl -k -s "http://$JENKINSIP:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)" --user "$USERNAME":"$USERPASS")
    curl -X POST "http://$JENKINSIP:8080/job/$TESTSUITE-thread$i/buildWithParameters?delay=0sec&TESTCASE=$TEST&token=$APITOKEN" -k -H "$CRUMB" --user "$USERNAME":"$USERPASS"
    echo "Test $TEST sent to Thread $i"
    sleep 1
done <"$TESTSUITE.conf"
