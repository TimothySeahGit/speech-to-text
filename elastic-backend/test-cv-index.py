from elasticsearch import Elasticsearch, helpers

# Create the elasticsearch client.
es = Elasticsearch("http://localhost:9200")

result = es.search(
 index='cv-transcriptions-4',
  query={
    'match': {'text': 'prognostications'}
  }
 )

print(result['hits']['hits'])