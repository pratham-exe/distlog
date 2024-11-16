from kafka import KafkaConsumer, KafkaProducer
import json
import sys
import time
import threading

topic_sub = "nodes"
consumer = KafkaConsumer(topic_sub, value_deserializer = lambda m: json.loads(m.decode('ascii')))
producer = KafkaProducer(value_serializer = lambda m: json.dumps(m).encode('ascii'))

topic_pub_1 = "storage"
topic_pub_2 = "alert"

node_heartbeats = {}
lock = threading.Lock()  # To manage concurrent access to shared data

def monitor_heartbeats():
    while True:
        time.sleep(7)  # Check every 10 seconds
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
        else:
            continue
           
    with lock:
        if message_type == "HEARTBEAT":
            node_heartbeats[node_id] = time.time()
    
    if message_type == "WARN" or message_type == "ERROR":
        producer.send(topic_pub_2, message)
        print(message)
    
    producer.send(topic_pub_1, message)
