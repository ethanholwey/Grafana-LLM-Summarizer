# Overview

Creating a Docker Container image is necessary for easy and fast deployment across systems. For our use-case, this makes it easy to deploy our code in an Amazon EC2 instance. 

This folder contains the environment for building the docker container image. We wrote a `dockerfile` to define what commands would run on container deployment, and what commands would be executed upon building the container. 

We based the container off of the default Python 3 docker container. We include a requirements.txt file within our container image and make `pip` install all of the default dependenices into the Docker container per the building instructions in the dockerfile.

# Building the image 

```docker build --no-cache -t grafana-llm:latest -t grafana-llm .```

This command builds the image using the instructions in the `dockerfile`. 

# Exporting the image

Once the image has been built it can be tagged with the following command: 

```docker tag grafana-llm:latest grafana-llm:0.0.1```

Then exported with: 

```docker save -o grafana-llm.tar grafana-llm:0.0.1```

An exported image can be moved and migrated to another machine for easy deployment, or uploaded to a Docker image repo. 

# Importing the image 

The exported image can be loaded on another machine by typing the following command: 

```docker load -i grafana-llm.tar```

Once loaded, the container can be deployed by creating a directory with the `docker-compose.yml` file. Please see the main README.md for deployment information.

    