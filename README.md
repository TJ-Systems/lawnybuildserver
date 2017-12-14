These scripts will create a 'build' server in which we can execute the build scripts from. 

gcpbuildserver.py
Image_project: debian-cloud
Image_family: debian-8
Machine_type: n1-standard-1


Installed packages and components:
 - Google SDK
 - Python 2.7
 - PIP
 - Google Python Libraries

Environmental Variables:
 GOOGLE_APPLICATION_CREDENTIALS=file.json
 GOOGLE_PROJECT=projectID
 GOOGLE_ZONE=zone
 PATH = local_repo_base

Startup Script (sscript.sh)
 - Install required software
 - set the environmental variables
 - establish the SSH keys for github repo(s)
 - Download the git repos
 - Build the DevOps network
  - Validate the network
 - Build the DevOps DNS
  - Validate DNS
 - Build the DevOps Load balancers
  - Validate the Load Balancers
 - Build the DevOps firewall rules
  - Validate the firewalls
 - Build the DevOps instance groups
  - Validate the instance groups
  - Build the Kubernetes Nodes
  - Validate Kubernetes
 - Build the terraform server
  - Validate the terraform server
 - Build the ElasticSearch Nodes
  - Validate ElasticSearch
 - Build the Logstash Nodes
  - Validate Logstash
 - Build the Kibana Nodes
  - Validate Kibana
 - Build the Jenkins Nodes
  - validate Jenkins
 - Log Errors or Success
 - Wipe all local files
 
Cleanup.py
Execute command and Arguments:
 - ./build_server.py 'GOOGLE_PROJECT' --zone 'GOOGLE_ZONE' --name lawnybuildserver0