import json
from json import loads
from flask import Flask, Response
from config import kafka_config
from kafka import KafkaConsumer, TopicPartition
from flask_cors import CORS



app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'

CORS(app)

@app.route('/consume/<symbol>/<offset>', methods=['GET', 'POST'])
def task_consume(symbol, offset):
    print("data", symbol, offset)
    def events():
        # global topic_offset
        topic_offset = 0
        print("topic_offset", topic_offset)
        if symbol != '':
            consumer = KafkaConsumer(
                                     bootstrap_servers=[kafka_config.get('bootstrap.servers')],
                                      # auto_offset_reset='latest',
                                      auto_offset_reset='earliest',
                                     value_deserializer=lambda x: loads(x.decode('utf-8')))
            tp = TopicPartition(symbol, topic_offset)
            # register to the topic
            consumer.assign([tp])
            # obtain the last offset value
            consumer.seek_to_end(tp)
            lastOffset = consumer.position(tp)
            consumer.seek_to_beginning(tp)
            print(f"{symbol} stock topic of offset {lastOffset}")
            for message in consumer:
                # print("message", message)
                value = json.dumps(message.value)
                topic_offset = message.offset
                partition = message.partition
                message = message.value
                message['offset'] = topic_offset
                message['symbol'] = symbol
                # time.sleep(1)
                yield 'data: {}\n\n'.format(json.dumps(message))
            # consumer.close()
    return Response(events(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)