export REPOSITORY=hydroshare
cd sim-users
bash build-push-images.sh
bash hub-up.sh 0 2  # 2 chrome instances
