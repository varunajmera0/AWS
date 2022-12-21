from json import dumps
from threading import Thread
import yfinance as yf
from yfinance import set_tz_cache_location
from flask import Flask, request
import awswrangler as wr
import boto3
import time
from config import boto_args, kafka_config
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'

CORS(app)

admin_client = KafkaAdminClient(
    bootstrap_servers=kafka_config.get('bootstrap.servers'),
)

producer = KafkaProducer(bootstrap_servers=kafka_config.get('bootstrap.servers'),
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

def task_producer(records, symbol):
    topics = admin_client.list_topics()
    print("List of topics: ", topics)
    print("Symbol: ", symbol)
    if symbol not in topics:
        topic_list = []
        topic_list.append(NewTopic(name=symbol, num_partitions=1, replication_factor=1))
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print("After adding list of topics: ", admin_client.list_topics())

    for record in records:
        producer.send(symbol, value=record)
    return True


def task(symbol):
    # set_tz_cache_location('/Users/theflash/Downloads')
    bucket = 'stock-bronze-layer'
    while True:
        current_data = yf.download(tickers=symbol, period="1d", interval="1m")
        current_data.reset_index(inplace=True)
        print("symbol download: ", symbol)
        current_data.columns = ["Datetime", "Open_drop", "High_drop", "Low_drop", "Close_drop", "Adj_Close", "Volume_drop"]
        path = f"s3://{bucket}/{symbol}/{symbol}.parquet"
        my_session = boto3.Session(**boto_args)
        object_exist = wr.s3.does_object_exist(path, boto3_session=my_session)

        if not object_exist:
            wr.s3.to_parquet(current_data,
                             path,
                             boto3_session=my_session,
                             )
            current_data['Datetime'] = current_data['Datetime'].astype(str)
            # task_producer(current_data.to_dict(orient='records'), symbol)
            # old_data = wr.s3.read_parquet([path], boto3_session=my_session)
        else:
            # print("=" * 30)
            old_data = wr.s3.read_parquet([path], boto3_session=my_session)
            # perform outer join
            current_outer = current_data.merge(old_data, how='left', indicator=True, on='Datetime', suffixes=('', '_remove'))
            # print("Both join DF", current_outer)
            # Drop the duplicate columns
            current_outer.drop([col for col in current_outer.columns if 'remove' in col], axis=1, inplace=True)
            # perform anti-join
            left_anti_join = current_outer[(current_outer._merge == 'left_only')].drop('_merge', axis=1)
            wr.s3.to_parquet(current_data,
                             path,
                             boto3_session=my_session,
                             )
            left_anti_join['Datetime'] = left_anti_join['Datetime'].astype(str)
            task_producer(left_anti_join.to_dict(orient='records'), symbol)
        time.sleep(30)


@app.route('/', methods=['GET', 'POST'])
def symbol_price():
    json = request.json
    symbol = json.get("symbol")
    print("symbol: ", symbol)
    t1 = Thread(target=task, kwargs={'symbol': symbol})
    # start the threads
    t1.start()
    return "Waah!"


if __name__ == '__main__':
    app.run(debug=True)