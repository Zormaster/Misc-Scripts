#!/usr/bin/python3

import requests
from contextlib import closing
import csv
import pandas as pd
from io import StringIO
from datetime import timedelta
from datetime import datetime
from ip2geotools.databases.noncommercial import DbIpCity
import json

# Codefresh API info
BASE_URL = "https://g.codefresh.io"
HEADERS = {
    'X-API-KEY': "zn8...",
    'Authorization': '821...'
}

# Cyops API Info
USERNAME = ""
PASSWORD = ""
HOSTNAME = ""

credentials = {  # this is for the API call.
    'credentials': {
        'loginid': USERNAME,
        'password': PASSWORD
    }
}

auth_response = requests.post('https://{}/auth/authenticate'.format(HOSTNAME),
                            data=json.dumps(credentials),
                            headers={},
                            verify=False)

token = json.loads(auth_response.text)['token']
headers = {"Authorization": "Bearer {}".format(token)}


def download_audit():
    url = f"{BASE_URL}/api/audit/download"

    r = requests.get(url=url, headers=HEADERS)
    data = r.text
    r.close()
    df = pd.read_csv(StringIO(data))

    mask = (df['action'] == 'login')
    df = df.loc[mask]

    df['createdAt'] = pd.to_datetime(df['createdAt'], format='%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)')
    startdate = datetime.now() - timedelta(hours=1)
    mask = (df['createdAt'] >= startdate)
    df = df.loc[mask]
    
    df = df.drop(labels=['id','correlationId'], axis=1)

    return df

def get_country(ip):
    response = DbIpCity.get(ip, api_key='free')
    return response.country

def create_alert(alert, headers):
    alert = requests.post('https://{}/api/3/alerts?'.format(HOSTNAME),
                            data=json.dumps(alert),
                            headers=headers,
                            verify=False)
    return alert


if __name__ == '__main__':

    df = download_audit()
    
    for k, i in df.iterrows():
        country = get_country(i['ip'])
        if country != 'US':
            alert = {
                "name": "Codefresh Authentication",
                "source": i['userName'],
                "company": "",
                "country": country,
                "severity": "/api/3/picklists/7efa2220-39bb-44e4-961f-ac368776e3b0",
                "sourceIP": i['ip'],
                "status": "/api/3/picklists/7de816ff-7140-4ee5-bd05-93ce22002146",
                "techName": "Codefresh",
                "userName": i['userName'],
                "virusTotal": "https://www.virustotal.com/gui/ip-address/" + i['ip'] + "/detection",
                "description": "<p><strong>Suspicious Codefresh Authentication</strong></p>",
                "extDescription": "<p>Source IP: " + str(i['ip']) + "<br />Source IP Country: " 
                    + country + "<br />Response Code: " + str(i['rs_status']) 
                    + "<br /><br />User ID: " + str(i['userId']) + "<br />Account ID: " 
                    + str(i['accountId']) + "<br />Entity: " + str(i['entity']) 
                    + "<br />Entity ID: " + str(i['entityId']) + "<br />Action: " 
                    + str(i['action']) + "<br />Request Query: " + str(i['req_query']) 
                    + "<br />Request Parameters: " + str(i['req_params']) 
                    + "<br />Request Headers: " + str(i['req_headers']) + "<br />Request URL: " 
                    + str(i['req_url']) + "<br /><br />Response Body: " + str(i['res_body']) 
                    + "<br />Response Status: " + str(i['rs_status']) + "<br />Created At: " 
                    + i['createdAt'].strftime('%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)') 
                    + "<br />User Email: " + i['userEmail'] + "<br />Entity Name: " + i['entityName'] 
                    + "<br />Logged In By Admin ID: " + str(i['loggedInByAdminId']) 
                    + "<br />Logged In By Admin Name: " + str(i['loggedInByAdminName']) + "</p>"
            }

            create_alert(alert, headers)
