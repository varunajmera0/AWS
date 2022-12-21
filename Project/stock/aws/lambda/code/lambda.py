import awswrangler as wr
from kafka import KafkaConsumer
from kafka import KafkaProducer
from time import sleep
from json import dumps
import json, boto3
from decimal import Decimal


import yfinance as yf
from yfinance import set_tz_cache_location
set_tz_cache_location('/tmp')
read = boto3.resource("dynamodb")

read = read.Table("stock_info")
                         
lambda_client = boto3.client('lambda')
GET_RAW_PATH = "/getSymbol"
CREATE_RAW_PATH = "/createSymbol"

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def lambda_handler(event, context):
    # TODO implement
    # print("event", event)
    if event['rawPath'] == GET_RAW_PATH:
        symbol = event['queryStringParameters']['symbol']
        print("symbol", symbol)
        data = read.get_item(Key={'symbol': symbol})
        return {
            'statusCode': 200,
            'headers': {
          'Access-Control-Expose-Headers': 'Access-Control-Allow-Origin',
          'Access-Control-Allow-Credentials': True,
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
            'body': json.dumps(data, cls=JSONEncoder)
        }
    elif event['rawPath'] == CREATE_RAW_PATH:
        # print("Decoded", json.loads(event.get("body")))
        decoded_event = event
        if "body" in event:
            decoded_event = json.loads(event.get("body"))
        
        item = read.get_item(Key={'symbol': decoded_event.get("symbol")}).get("Item", {})
        print("item.get('symbol')")
        if item.get('symbol') is None:
            msft = yf.Ticker(decoded_event.get("symbol"))
            item = json.loads(json.dumps(msft.info), parse_float=Decimal)
            item['symbol'] = decoded_event.get("symbol")
            read.put_item(Item=item)
        data = read.get_item(Key={'symbol': decoded_event.get("symbol")})
        return {
            'statusCode': 200,
            'headers': {
                  'Access-Control-Expose-Headers': 'Access-Control-Allow-Origin',
                  'Access-Control-Allow-Credentials': True,
                  'Content-Type': 'application/json',
                  'Access-Control-Allow-Origin': '*',
             },
            'body': json.dumps(data, cls=JSONEncoder)
        }
