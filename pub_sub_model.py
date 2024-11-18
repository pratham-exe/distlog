from kafka import KafkaConsumer, KafkaProducer
from log import generate_microservice_log
import json
import sys
import time
import threading

topic_sub = sys.argv[1]
consumer = KafkaConsumer(topic_sub, value_deserializer = lambda m: json.loads(m.decode('ascii')))
producer = KafkaProducer(value_serializer = lambda m: json.dumps(m).encode('ascii'))

topic_pub_1 = sys.argv[2]
topic_pub_2 = sys.argv[3]

node_heartbeats = {}
lock = threading.Lock()

def monitor_heartbeats():
    while True:
        time.sleep(6)
        with lock:
            current_time = time.time()
            for node_id, last_heartbeat in list(node_heartbeats.items()):
                if current_time - last_heartbeat > 7:
                    print(f"ALERT: Node {node_id} missed its heartbeat!")

monitor_thread = threading.Thread(target=monitor_heartbeats, daemon=True)
monitor_thread.start()

registered_nodes = []

for message in consumer:
    node_id = message.value['node_id']
    message_type = message.value['message_type']
    if node_id not in registered_nodes:
        if message_type == "REGISTRATION":
            registered_nodes.insert(0, node_id)
            node_heartbeats[node_id] = time.time()
            reg_log = generate_microservice_log(message.value)
            producer.send(topic_pub_1, reg_log)
        continue

           
    with lock:
        if message_type == "HEARTBEAT":
            node_heartbeats[node_id] = time.time()
    
    if 'log_level' in message.value:
        log_level = message.value['log_level']
        if log_level == "WARN":
            producer.send(topic_pub_2, message.value)
        if log_level == 'ERROR':
            producer.send(topic_pub_2, message.value)
            dereg_log = generate_microservice_log(message.value)
            producer.send(topic_pub_1, dereg_log)
            registered_nodes.remove(message.value['node_id'])
            continue
    
    producer.send(topic_pub_1, message.value)
