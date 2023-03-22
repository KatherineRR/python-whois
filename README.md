
# Automation Programming Assignment


To run the project:

- Open /app/.env and modify it by adding your api key, source email and password, destination emails, smtp server and port
- Open /app/domains.yml and add your domains
- From the command line open the directory of your project
```
cd python-whois
```
- Create a docker image   
```
docker build -t python-whois .
```
-  Create and start a new Docker container from your docker image
```
docker run python-whois    
```
