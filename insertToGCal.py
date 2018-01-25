# -*- coding: utf-8 -*-
from __future__ import print_function
import httplib2
import os
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.errors import HttpError
from time import sleep

import datetime

from regex import *
from lxml import html, etree
import requests


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Lectio To Google Calender'
USER_DATA = json.load(open('users.json'))

all_credential = []
all_http = []
all_service = []

all_events = []

def get_credentials(filename):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   filename)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def addAllEvents(service, calID):
    for x in range(len(all_events)):
        try:
            #service.events().delete(calendarId=calID, eventId=all_events[x]["id"]).execute()
            event = service.events().update(calendarId=calID, eventId = all_events[x]["id"], body = all_events[x]).execute()
            print('Updated event: ', (event.get('htmlLink')))
        except HttpError:
            event = service.events().insert(calendarId=calID, body = all_events[x]).execute()
            print('Event created: ', (event.get('htmlLink')))
        sleep(0.5) #Rate limit handler
        
def retrieve(GymID, StudentID, Week, Year):
    tree_list = []
    for x in range(1, 52):
        if x < 10:
            x = "0" + str(x)
        else:
            x = str(x)
        page = requests.get('https://www.lectio.dk/lectio/'+GymID+'/SkemaNy.aspx?type=elev&elevid='+StudentID+'&week='+x+Year)
        tree_list.append(html.fromstring(page.content))
    return tree_list

def createEvent(uid, startTime, endTime, summary, location, description):
    newEvent = {
        'id' : uid,
        'start' : {
            'dateTime' : startTime,
            'timeZone' : 'Europe/Copenhagen',
        },
        'end' : {
            'dateTime' : endTime,
            'timeZone' : 'Europe/Copenhagen',
        },
        'summary' : summary,
        'location' : location,
        'description' : description
    }

    all_events.append(newEvent)
def main():
    global all_events
    for x in range(len(USER_DATA["users"])):
        all_credential.append(get_credentials(USER_DATA["users"][x]["credentialFileName"]))
        all_http.append(all_credential[x].authorize(httplib2.Http()))
        all_service.append(discovery.build('calendar', 'v3', http=all_http[x]))
        calID = USER_DATA["users"][x]["calID"]
        document = retrieve(USER_DATA["users"][x]["gymID"], USER_DATA["users"][x]["elevID"], "04", "2018")
        modules = []
        for tree in document:
            modules += tree.xpath('/html/body/div/form/section/div/div/table/tr[4]/td/div/a/@data-additionalinfo')
        
        for y in range(len(modules)):
            summary = getStatus(modules[y]) + getTeam(modules[y]) + " - " + getTeacher(modules[y])
            location = getRoom(modules[y])
            description = getTitle(modules[y]) + "\n" +getNote(modules[y]) + "\n" + getAdditionalContent(modules[y])
            print(getTime(modules[y]))
            time = getTime(modules[y]).split(' til ')
            tempDate = getDate(modules[y])
            if(len(tempDate.split('/')[1].split('-')[0])==2):
                month = tempDate.split('/')[1].split('-')[0]
            else:
                month = '0'+tempDate.split('/')[1].split('-')[0]
            if(len(tempDate.split('/')[0])==2):
                day = tempDate.split('/')[0]
            else:
                day = '0'+tempDate.split('/')[0]

            date = tempDate.split('-')[1]+'-'+ month +'-'+ day
            StartTime = date +'T'+ time[0]+':00'#yyyy-mm-ddTtt:mm:ss
            EndTime = date +'T'+ time[1]+':00'#yyyy-mm-ddTtt:mm:ss
            createEvent(10000 + y, StartTime, EndTime, summary, location, description)
        addAllEvents(all_service[x], calID)
        all_events = []

if __name__ == '__main__':
    main()
