from elasticsearch import Elasticsearch
import sys

check = sys.argv[1]

elastic_password = "UuqL5r5huS5fpNcreeU2"
es = Elasticsearch(
    "https://localhost:9200",
    ca_certs="~/elasticsearch-8.16.0/config/certs/http_ca.crt",
    basic_auth=("elastic", elastic_password)
)

if check == "REGISTRATION" or check == "HEARTBEAT":
    query = {
        "query": {
            "match": {
                "message_type": check
            }
        }
    }
else:
    query = {
        "query": {
            "match": {
                "log_level": check
            }
        }
    }

response = es.search(index="logs", body=query)

print(f"Search results for {check}:")
for hit in response['hits']['hits']:
    print(hit['_source'])
