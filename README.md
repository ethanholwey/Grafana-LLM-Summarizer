# Grafana LLM Summarizer

This project utilizes integrates OpenAI's API as well as FastAPI to integrate LLM-summarization into the free-use version of Grafana. 

The final deliverable of this project is a Docker container image that can be deployed on various types on-premises servers, or cloud computing platforms. 

### Note: This Documentation page is subject to change as we continue to develop our project and all features described on this page may not have full functionality until our project is complete. 

## Deploying the Docker container: 

A Docker container image is packaged with a Python environment, necessary OpenAI libraries, and our script that builds the API with FastAPI and UviCorn. 

An environment variable `API_KEY` has been defined in our Docker container image. The following command can be executed to deploy the docker container provided the image is present: 

```
docker run -d -e API_KEY=OPENAI_API_KEY_HERE -p 8000:8000 ai-agent --restart unless-stopped
```

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


