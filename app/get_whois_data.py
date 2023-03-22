import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.request import urlopen
from dotenv import load_dotenv

load_dotenv()

def get_whois_data(domain):
    try:
        url = 'https://www.whoisxmlapi.com/whoisserver/WhoisService'
        params = {
            'apiKey': os.environ.get('API_KEY'),
            'domainName': domain,
            'outputFormat': 'JSON'
        }
        query_string = '&'.join([f'{key}={value}' for key, value in params.items()])
        response = urlopen(f'{url}?{query_string}')
        data = json.loads(response.read())
        return data
    except Exception as e:
        raise Exception("Failed to retrieve WHOIS data", e)

def process_domain(domain):
    try:
        data = [''] * 9
        json_data = get_whois_data(domain)
        error = json_data['WhoisRecord'].get('dataError') or ''
        data[0] = domain

        if (error == ''):
            data[1] = json_data['WhoisRecord']['registryData'].get('createdDate') or ''
            data[2] = json_data['WhoisRecord']['registryData'].get('updatedDate') or ''
            data[3] = json_data['WhoisRecord']['registryData'].get('expiresDate') or ''
            if (json_data['WhoisRecord'].get('registrant')):
                data[4] = json_data['WhoisRecord'].get('registrant').get('name') or ''
                data[5] = json_data['WhoisRecord'].get('registrant').get('email') or ''
            if (json_data['WhoisRecord'].get('administrativeContact')):
                data[6] =  json_data['WhoisRecord'].get('administrativeContact').get('email') or ''
            if(json_data['WhoisRecord'].get('technicalContact')):
                data[7] = json_data['WhoisRecord'].get('technicalContact').get('email') or ''
            data[8] = json_data['WhoisRecord'].get('contactEmail') or ''

        return data

    except Exception as e:
        raise Exception("Failed to retrieve WHOIS data", e)
    
def send_email(domain, message):
    try: 
        from_addr = os.environ.get('SOURCE_EMAIL')
        to_addr = os.environ.get('DESTINATION_EMAIL')
        password = os.environ.get('SOURCE_EMAIL_PASS')
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = f'{domain} WHOIS Record Update'
        msg.attach(MIMEText(message, "plain"))
        server = smtplib.SMTP(os.environ.get('SMTP_SERVER'),os.environ.get('SMTP_PORT'))
        server.starttls()
        server.login(from_addr, password)
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
        server.quit()
    except smtplib.SMTPException as error:
        print("Error while connecting to smtp server", error)