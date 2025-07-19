# distlog

distlog is a distributed logging and monitoring system that simulates multiple microservice nodes, collects their logs and heartbeats, processes them through a Kafka-based pub-sub model, and stores them in Elasticsearch. It also provides alerting and search capabilities for log data.

## Architecture

- **Node Simulators (`node1.py`, `node2.py`, `node3.py`)**: Simulate different microservices (Payment, Order, Service). Each node:

  - Registers itself with the system.
  - Sends periodic heartbeat messages.
  - Generates logs of varying severity (INFO, WARN, ERROR).
  - Sends logs and heartbeats to a Fluentd HTTP endpoint.

- **Heartbeat (`heartbeat.py`)**: Defines the function to send heartbeat messages from nodes.

- **Log Generation (`log.py`)**: Contains functions to generate logs of different types and severities, as well as registration logs.

- **Fluentd Configuration (`fluent.conf`)**: Sets up Fluentd to receive logs via HTTP and forward them to a Kafka topic.

- **Pub-Sub Model (`pub_sub_model.py`)**:

  - Consumes messages from a Kafka topic.
  - Monitors node heartbeats and raises alerts if a node misses a heartbeat.
  - Forwards logs and registration events to other Kafka topics.
  - Handles node registration and deregistration.

- **Log Storage (`log_storage.py`)**:

  - Consumes logs from Kafka and stores them in Elasticsearch.
  - Prints confirmation or errors for each log stored.

- **Alert System (`alert_system.py`)**:

  - Consumes alert messages from Kafka and prints them.

- **Elasticsearch Utilities**:
  - `search_es_storage.py`: Searches logs in Elasticsearch by type or log level.
  - `delete_es_storage.py`: Deletes all documents in the Elasticsearch logs index.

## Setup

### Prerequisites

- Python 3.x
- Kafka
- Elasticsearch 8.x
- Fluentd
- Python packages: `kafka-python`, `elasticsearch`, `requests`

### Installation

1. Install required Python packages:
   ```bash
   pip install kafka-python elasticsearch requests
   ```
2. Set up and start Kafka and Elasticsearch servers.
3. Configure Fluentd using the provided `fluent.conf` file:
   - Receives logs via HTTP on port 9880 and forwards them to the Kafka topic `nodes`.

## Usage

### Simulate Nodes

Run each node in a separate terminal:

```bash
python node1.py
python node2.py
python node3.py
```

### Start Pub-Sub Model

```bash
python pub_sub_model.py nodes processed_logs alerts
```

- `nodes`: Kafka topic to subscribe to (input)
- `processed_logs`: Kafka topic to publish processed logs
- `alerts`: Kafka topic to publish alerts

### Store Logs in Elasticsearch

```bash
python log_storage.py processed_logs
```

### Run Alert System

```bash
python alert_system.py alerts
```

### Search Logs in Elasticsearch

```bash
python search_es_storage.py <LOG_LEVEL|REGISTRATION|HEARTBEAT>
```

- Example: `python search_es_storage.py ERROR`

### Delete All Logs in Elasticsearch

```bash
python delete_es_storage.py
```

## File Descriptions

- `node1.py`, `node2.py`, `node3.py`: Simulate different service nodes.
- `heartbeat.py`: Heartbeat message sender.
- `log.py`: Log and registration message generator.
- `fluent.conf`: Fluentd configuration for log forwarding.
- `pub_sub_model.py`: Kafka-based pub-sub logic and heartbeat monitoring.
- `log_storage.py`: Stores logs in Elasticsearch.
- `alert_system.py`: Consumes and prints alerts.
- `search_es_storage.py`: Searches logs in Elasticsearch.
- `delete_es_storage.py`: Deletes all logs from Elasticsearch.
