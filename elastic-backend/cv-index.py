from elasticsearch import Elasticsearch, helpers
import csv

mappings = {
            "properties": {
                "duration": {
                    "type": "float"
                },
                "up_votes": {
                    "type": "integer"
                },
                "down_votes": {
                    "type": "integer"
                },
                "generated_text": {
                    "type": "text"
                },
                "age": {
                    "type": "text"
                },
                "gender": {
                    "type": "text"
                },
                "accent": {
                    "type": "text"
                }
            }
        }

index_name = 'cv-transcriptions-float'

# Create the elasticsearch client.
es = Elasticsearch("http://localhost:9200")
es.options(ignore_status=[400,404]).indices.delete(index=index_name)
es.indices.create(index=index_name, mappings=mappings)

# Open csv file and bulk upload
with open('./data/cv-valid-dev.csv') as f:
    reader = csv.DictReader(f)
    # print(list(reader)[:5])
    for row in reader:
        # print(row)
        
        print(row)
        es.index(index=index_name,
                document=row)
    # helpers.bulk(es, reader, index='cv-transcriptions')