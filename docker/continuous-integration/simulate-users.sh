export REPOSITORY=hydroshare
cd sim-users
bash build-push-images.sh
bash hub-up.sh 0 2  # 2 chrome instances
cd ..
HUBIP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' sim-users_selenium-hub_1 | sed 's/\./\\\./g')  # get Hub IP and escape periods
find ./jenkins/jobs/ -name "*.xml" | xargs -i sed -i "s/--grid localhost/--grid $HUBIP/g" {}  # replace localhost grid setting with hub ip
