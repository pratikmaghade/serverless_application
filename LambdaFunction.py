import json
import boto3
import time
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Product')

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

def lambda_handler(event, context):
    if event['operation'] == 'addProduct':
        return saveProduct(event)
    else:
        return getProducts()

def saveProduct(event):
    gmt_time = time.gmtime()
    now = time.strftime('%a, %d %b %Y %H:%M:%S', gmt_time)

    # Ensure the price is converted to Decimal
    price = Decimal(str(event['price']))

    table.put_item(
        Item={
            'productCode': event['productCode'],
            'price': price,
            'createdAt': now
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Product with ProductCode: ' + event['productCode'] + ' created at ' + now)
    }

def getProducts():
    response = table.scan()
    items = response['Items']
    print(items)
    
    return {
        'statusCode': 200,
        'body': json.dumps(items, default=decimal_default),  # Use the custom serializer here
        'headers': {
            'Content-Type': 'application/json',
        }
    }
