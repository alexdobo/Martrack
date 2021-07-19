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


def portsGet():
    client = boto3.resource('dynamodb')
    ports = client.Table('martrackPort')
    table = ports.scan()
    data = table['Items']
    while 'LastEvaluatedKey' in table:
        table = ports.scan(ExclusiveStartKey=table['LastEvaluatedKey'])
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

def portPost(body):
    client = boto3.resource('dynamodb')

    ports = client.Table('martrackPort')
    response = ports.put_item(
       Item=body
   )
    return {
        'statusCode': 200,
        'body': 'Record ' + str(body['portId']) + ' added',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    

def portGet(portId):
    client = boto3.resource('dynamodb')
    ports = client.Table('martrackPort')
    data = ports.get_item(
        Key={
            'portId':int(portId)
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

def portPut(body,portId):
    client = boto3.resource('dynamodb')

    ports = client.Table('martrackPort')
    response = ports.put_item(
       Item=body
   )
    return {
        'statusCode': 200,
        'body': 'Record ' + str(body['portId']) + ' updated',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    return response

def portDelete(portId):
    client = boto3.resource('dynamodb')
    ports = client.Table('martrackPort')
    data = ports.delete_item(
        Key={
            'portId':int(portId)
        }
    )
    response = {
        'statusCode': 200,
        'body': 'Port ' + str(portId) + ' deleted.',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    return response