# GitHub Actions

GitHub actions in our workflow automates the creation of Docker Images that are pushed to Docker Hub. This allows for us to make changes to our code, and immediately verify that we are still able to create docker images with our freshly pushed changes.

## How it works

To use a GitHub action in a GitHub repository you must create a `.github\workflows` directory in the root of your repository. Here you can create YML files specifying details regarding your desired workflow. 

# `docker-image.yml`

Here we will breakdown the various sections needed in a YML file for a GitHub workflow, and the ones used for ours. 

## Name
At the top any GitHub action file, and ours, you specify the name of your workflow following the `name: ` field. This name will be what is displayed in the actions tab of your repository it **does not** look at the name of your .yml file for this information. 
```
name: Build and push docker image to dockerhub 
```
We just called our workflow what it does, which is building and pushing our Docker Image to Docker Hub.

## Workflow Trigger
For  our workflow, we wanted it to create and push docker images after a push is made to the main branch of our repository 
```
on: 
	push:
		branches:
			-main
```
## Jobs
The jobs section of this workflow is responsible for the building of the Docker Image and pushing it to Docker Hub:
```
jobs:
  publish_images:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build the Docker Image
        run: docker build ./Container-Building -t ethanholwey/grafana-llm:latest

      - name: Push Image to Docker Hub
        run: |
          docker login -u ethanholwey -p ${{ secrets.DOCKER_HUB_TOKEN}}
          docker push ethanholwey/grafana-llm:latest
```
First it pulls the source code into the GitHub Actions runner so the workflow can access our Dockerfile and build context

Then it uses `docker build` to create the image from the `./Container-Building` directory and tags it as `ethanholwey/grafana-llm:latest`

Next it authenticates with docker hub using the `DOCKER_HUB_TOKEN` which is a secret stored in our repository

Finally it pushes the newly built image to Docker Hub, making it available for deployment or pulling elsewhere, like our ec2 VM. 
