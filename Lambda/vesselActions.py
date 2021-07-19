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


def vesselsGet():
    client = boto3.resource('dynamodb')
    vessels = client.Table('martrackVessel')
    table = vessels.scan()
    data = table['Items']
    while 'LastEvaluatedKey' in table:
        table = vessels.scan(ExclusiveStartKey=table['LastEvaluatedKey'])
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

def vesselPost(body):
    client = boto3.resource('dynamodb')

    vessels = client.Table('martrackVessel')
    response = vessels.put_item(
       Item=body
   )
    return {
        'statusCode': 200,
        'body': 'Record ' + str(body['vesselId']) + ' added',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    

def vesselGet(vesselId):
    client = boto3.resource('dynamodb')
    vessels = client.Table('martrackVessel')
    data = vessels.get_item(
        Key={
            'vesselId':int(vesselId)
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

def vesselPut(body,vesselId):
    client = boto3.resource('dynamodb')

    vessels = client.Table('martrackVessel')
    response = vessels.put_item(
       Item=body
   )
    return {
        'statusCode': 200,
        'body': 'Record ' + str(body['vesselId']) + ' updated',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    return response

def vesselDelete(vesselId):
    client = boto3.resource('dynamodb')
    vessels = client.Table('martrackVessel')
    data = vessels.delete_item(
        Key={
            'vesselId':int(vesselId)
        }
    )
    response = {
        'statusCode': 200,
        'body': 'Vessel ' + str(vesselId) + ' deleted.',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    return response