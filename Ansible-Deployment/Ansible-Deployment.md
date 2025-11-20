## Overview

The Ansible playbook is intended to be placed in the same directory as the Docker Compose. The server runs the playbook from on the local EC2 instance. 

The Ansible playbook instructions include a check for installation of Docker and Docker Compose. Once Docker Compose is installed, it deploys the docker-compose file within the same directory that the Ansible playbook is contained in within the EC2 server. 

## Deployment with Ansible 
1. Ensure the docker-compose file within this repository is in the same folder as the Ansible deployment file.
2. Run the following command `ansible-playbook deploy.yml`
