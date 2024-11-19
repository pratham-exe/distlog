from elasticsearch import Elasticsearch

elastic_password = "UuqL5r5huS5fpNcreeU2"
es = Elasticsearch(
    "https://localhost:9200",
    ca_certs="~/elasticsearch-8.16.0/config/certs/http_ca.crt",
    basic_auth=("elastic", elastic_password)
)


response = es.delete_by_query(
    index="logs",
    body={
        "query": {
            "match_all": {}
        }
    }
)
print("Deleted documents:", response)
