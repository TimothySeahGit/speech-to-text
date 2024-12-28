from elasticsearch import Elasticsearch, helpers

# Create the elasticsearch client.
es = Elasticsearch("http://localhost:9200")

index_name = 'cv-transcriptions-float'


result = es.search(
 index=index_name,
  query={
    'match': {'generated_text': 'prognostications'}
  }
 )

print(result['hits']['hits'], '\n')


result = es.search(
 index=index_name,
  query={
    'range': {'duration':  {
        "gte": '7.01',
        "lte": '10.00'}
            }
        }
 )

print(result['hits']['hits'], '\n')


result = es.search(
 index=index_name,
  query={
    'match': {'age': 'twenties'}
  }
 )

print(result['hits']['hits'], '\n')


result = es.search(
 index=index_name,
  query={
    'match': {'gender': 'male'}
  }
 )

print(result['hits']['hits'], '\n')


result = es.search(
 index=index_name,
  query={
    'match': {'accent': 'england'}
  }
 )

print(result['hits']['hits'], '\n')

result = es.search(
 index=index_name,
  query={
    'multi_match': {'query': "prognos", 'type': "bool_prefix", 'fields': ["generated_text.suggest^1"]}
  }
 )

print(result['hits']['hits'], '\n')