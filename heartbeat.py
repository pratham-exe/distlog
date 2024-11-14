import time

def send_heartbeat(node_id):
    while True:
        heartbeat_message = {
            "node_id": node_id,
            "message_type": "HEARTBEAT",
            "status": "UP",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"Heartbeat: {heartbeat_message}")
        time.sleep(5) 
