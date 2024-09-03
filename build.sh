detached_mode=$detached_mode

# build base image with all dependencies
sudo docker build -f Dockerfile_django_base -t chat:django_base_latest .

if [ "$detached_mode" = "true" ]; then
    # build and start container in detached mode
    sudo docker-compose up --build -d
else
    # build and start container
    sudo docker-compose up --build
fi
