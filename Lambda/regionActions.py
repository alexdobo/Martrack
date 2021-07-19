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


def regionsGet():
    client = boto3.resource('dynamodb')
    regions = client.Table('martrackRegion')
    table = regions.scan()
    data = table['Items']
    while 'LastEvaluatedKey' in table:
        table = regions.scan(ExclusiveStartKey=table['LastEvaluatedKey'])
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

def regionPost(body):
    client = boto3.resource('dynamodb')

    regions = client.Table('martrackRegion')
    response = regions.put_item(
       Item=body
   )
    return {
        'statusCode': 200,
        'body': 'Record ' + str(body['regionId']) + ' added',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    

def regionGet(regionId):
    client = boto3.resource('dynamodb')
    regions = client.Table('martrackRegion')
    data = regions.get_item(
        Key={
            'regionId':int(regionId)
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

def regionPut(body,regionId):
    client = boto3.resource('dynamodb')

    regions = client.Table('martrackRegion')
    response = regions.put_item(
       Item=body
   )
    return {
        'statusCode': 200,
        'body': 'Record ' + str(body['regionId']) + ' updated',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    return response

def regionDelete(regionId):
    client = boto3.resource('dynamodb')
    regions = client.Table('martrackRegion')
    data = regions.delete_item(
        Key={
            'regionId':int(regionId)
        }
    )
    response = {
        'statusCode': 200,
        'body': 'Region ' + str(regionId) + ' deleted.',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    return response