import boto3
import json
from decimal import Decimal

def handle_decimal_type(obj):
  if isinstance(obj, Decimal):
      if float(obj).is_integer():
         return int(obj)
      else:
         return float(obj)
  raise TypeError


def routesGet():
    client = boto3.resource('dynamodb')
    routes = client.Table('martrackRoute')
    table = routes.scan()
    data = table['Items']
    while 'LastEvaluatedKey' in table:
        table = routes.scan(ExclusiveStartKey=table['LastEvaluatedKey'])
        data.extend(table['Items'])
    
    response = {
        'statusCode': 200,
        'body': json.dumps(data, default=handle_decimal_type),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    return response

def routePost(body):
    client = boto3.resource('dynamodb')

    routes = client.Table('martrackRoute')
    response = routes.put_item(
       Item=body
   )
    return {
        'statusCode': 200,
        'body': 'Record ' + str(body['routeId']) + ' added',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    

def routeGet(routeId):
    client = boto3.resource('dynamodb')
    routes = client.Table('martrackRoute')
    data = routes.get_item(
        Key={
            'routeId':int(routeId)
        }
    )
    response = {
        'statusCode': 200,
        'body': json.dumps(data['Item'], default=handle_decimal_type),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    return response

def routePut(body,routeId):
    client = boto3.resource('dynamodb')

    routes = client.Table('martrackRoute')
    response = routes.put_item(
       Item=body
   )
    return {
        'statusCode': 200,
        'body': 'Record ' + str(body['routeId']) + ' updated',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    return response

def routeDelete(routeId):
    client = boto3.resource('dynamodb')
    routes = client.Table('martrackRoute')
    data = routes.delete_item(
        Key={
            'routeId':int(routeId)
        }
    )
    response = {
        'statusCode': 200,
        'body': 'Route ' + str(routeId) + ' deleted.',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    return response