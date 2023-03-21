
# Automation Programming Assignment


To run the sample:

- Open /app/get_whois_data.py and modify the lines 49,50,56,58 with your source and destination emails, smtp server and port of your source email and password
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
