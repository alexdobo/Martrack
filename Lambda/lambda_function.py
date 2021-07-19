import boto3
import json
from vesselActions import *
from portActions import *
from routeActions import *
from regionActions import *


def lambda_handler(event, context):
    #return event
    try:
        body = json.loads(event['body'])
    except:
        body = False
    
    #changes ? to / and then splits
    path = event['requestContext']['http']['path'].replace('?','/').split('/')
    method = event['requestContext']['http']['method']

    destination = path[2] if len(path) > 2 else False
    

    #needs to be if path contains
    if destination == 'vessel':
        response = vessels(body, method, path)
    elif destination == 'route':
        response = route(body, method, path)
    elif destination == 'port':
        response = port(body, method, path)
    elif destination == 'region':
        response = region(body, method, path)
    else:
        response = {
            'statusCode':404,
            'body':''
        }
    print(response)
    return response

def vessels(body,method,path):
    response = {
        'statusCode':404,
        'body':''
    }
    if len(path) < 4: #doesn't have a vesselId in the path
        if (method == 'GET'):
            response = vesselsGet()
        elif method == 'POST':
            response = vesselPost(body)
    else:
        vesselId = path[3]
        if method == 'GET':
            response = vesselGet(vesselId)
        elif method == 'PUT':
            response = vesselPut(body, vesselId)
        elif method == 'DELETE':
            response = vesselDelete(vesselId)
    return response


def route(body,method,path):
    return false


def port(body,method,path):
    return false


def region(body,method,path):
    return false


