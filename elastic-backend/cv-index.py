from elasticsearch import Elasticsearch, helpers
import csv
import logging
logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

mappings = {"dynamic": "true",
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
                    "type": "text",
                    "fields": {
                        "suggest": {
                            "type": "search_as_you_type"
                        }
                    }
                }
            }
        }

index_name = 'cv-transcriptions-float'

# Create the elasticsearch client.
try:
    # es = Elasticsearch("http://localhost:9200")
    es = Elasticsearch("http://elastic-backend-1:9200")
    es.options(ignore_status=[400,404]).indices.delete(index=index_name)
    es.indices.create(index=index_name, mappings=mappings)
except Exception as e:
    logger.debug(e)

# Open csv file and bulk upload
with open('/usr/data/cv-valid-dev.csv') as f:
    reader = csv.DictReader(f)
    # print(list(reader)[:5])
    for row in reader:
        # print(row)
        
        print(row)
        logger.debug(row)
        es.index(index=index_name,
                document=row)
    # helpers.bulk(es, reader, index='cv-transcriptions')