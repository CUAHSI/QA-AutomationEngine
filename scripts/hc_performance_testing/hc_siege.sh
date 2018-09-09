#!/usr/bin/env bash

# 1) 'Siege' HydroClient with 1 concurrent user (c1), repeat 10 times (r10),
# set delay between repetitions to up to 1 second (d1) and write results to a specified log file.
# 2) 'Siege' HydroClient with 2 concurrent users, but now repeat this for 30 seconds (t30s)

# Add sessionid cookies as needed with:
# --header="Cookie: sessionid=mjifge6nj0mo6375cdlf2rvw5dea0pr3" 
echo 'HYDROCLIENT' > hc_siege.txt

siege -c1 -r10 -d1 --log=/dev/null http://data.cuahsi.org \
 --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36" \
 --header="Accept: text/html"  >> /dev/null 2>> hc_siege.txt & wait

siege -c2 -t30s -d1 --log=/dev/null http://data.cuahsi.org \
 --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36" \
 --header="Accept: text/html"  >> /dev/null 2>> hc_siege.txt & wait
