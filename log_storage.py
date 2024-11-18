from kafka import KafkaConsumer
import json
from elasticsearch import Elasticsearch
import sys

elastic_password = "UuqL5r5huS5fpNcreeU2"
es = Elasticsearch(
    "https://localhost:9200",
    ca_certs="~/elasticsearch-8.16.0/config/certs/http_ca.crt",
    basic_auth=("elastic", elastic_password)
)

topic_sub = sys.argv[1]
consumer = KafkaConsumer(topic_sub, value_deserializer=lambda m: json.loads(m.decode('ascii')))

def store_log(log_data):
    try:
        es.index(index="logs", document=log_data)
        if "log_id" in log_data:
            print(f"Log stored successfully: {log_data['node_id']}, {log_data['log_id']}, {log_data['log_level']}")
        else:
            print(f"Log stored successfully: {log_data['node_id']}, {log_data['message_type']}")
    except Exception as e:
        print(f"Error storing log: {e}")

for message in consumer:
    store_log(message.value)
