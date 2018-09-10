export REPOSITORY=hydroshare
bash sim-users/build-push-images.sh
bash sim-users/hub-up.sh 0 2  # 2 chrome instances
