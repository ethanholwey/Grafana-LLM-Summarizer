# Grafana LLM Summarizer

This project utilizes integrates OpenAI's API as well as FastAPI to integrate LLM-summarization into the free-use version of Grafana. 

The final deliverable of this project is a Docker container image that can be deployed on various types on-premises servers, or cloud computing platforms. 


## Ansible Deployment

The Ansible playbook contained within this repository under `Ansible-Deployment\playbook.yml` is designed to: 
1. Install Docker, Python, any necessary dependencies. 
2. Deploy the Docker-Compose stack required for Grafana-LLM.
3. Deploy Grafana 

An example of deploying Grafana-LLM on a Debian-based Linux Amazon E2 VM is below: 
1. Install Ansible with `sudo apt install ansible -y`
2. Create a folder in the home directory titled `"ansible"`. Include both the `docker-compose.yml` file and `playbook.yml` file from `Ansible-Deployment\playbook.yml` in this folder. 
4. Run the following command: 
```ansible-playbook playbook.yml```
5. When prompted, enter the OpenAI API Key

## Standalone Docker Compose Deployment: 

If you would like to manually deploy the Grafana-LLM image via Docker-Compose (without Ansible), drag the `docker-compose.yml` file to a folder and run the following command: 
```docker-compose.yml up -d```

The Docker container image is packaged with a Python environment, necessary OpenAI libraries, and our script that builds the API with FastAPI and UviCorn. 

An environment variable `API_KEY` has been defined in our Docker container image. An example `docker-compose` file can be found below:


Within the local `logs` directory that this container is deployed in, the LLM will summarize any log files present within this folder. 

This command deploys the API agent in the background on port 8000. 

## Utilizing the API

Once the Docker container is deployed, the API will be available from the following endpoints:
- `/file`: Parses a text/log file into `.json` formatting.
- `/count`: Counts all the text/log files and parses them while searching for key logging phrases (i.e., "criticial", "warning", etc). Categorizes the log files based on that.
- `/`: Root endpoint, what is immediately displayed upon accessing the API in the browser. This endpoint displays `.json ` formatting of a log summary after making another API call to OpenAPI's GPT-4o LLM. 

### Setting up initial Grafana Dashboard: 

A dashboard was setup in Grafana by taking the following steps: 
1. Open Grafana --> Click "Dashboards" --> Click "Edit" to edit the panel.
2. Under "Queries", change the "Type" to "JSON". Change the method to "GET" and set the URL to the IP/FQDN of the host machine the Grafana API Summarizer API is running on and port `(default: 8000)`.

### Setting up a pie chart in Grafana for categorized log view
1. Repeat steps 1-2 above, change the URL to have the `/count` endpoint (i.e, 127.0.0.1:8000/count)
2. Change the visualization to a pie chart. 

## Endpoints
We created three different endpoints that are key compontnets to our application. They are all accessed via the IP address of our EC2 Instance (i.e, 127.0.0.1:8000/<Endpoint name>
### Endpoint 1 - / (root)
Our Root endpoint hosts the LLM's summary. Once you access this enpoint, the LLM will start reading the file and generating a summary. The summary is then displayed in JSON format on the webpage. 

### Endpoint 2 - /file 
The file endpoint hosts the entire file that the LLM is using to summarize. The file's content is displayed in JSON format on the webpage
### Endpoint 3 - /count
The count endpoint hosts key value pairs for defined keywords that are important in logs. The purpose of this endpoint is to read the file and count how many times a keyword appears in the log. We have a few keywords defined and the webpage displays key value pairs in the following format:
Good: 2,
Failed: 0
Critical: 34




