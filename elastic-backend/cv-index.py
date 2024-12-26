from elasticsearch import Elasticsearch, helpers
import csv

# Create the elasticsearch client.
es = Elasticsearch("http://localhost:9200")

es.indices.create(index='cv-transcriptions-4')

# Open csv file and bulk upload
with open('./data/cv-valid-dev.csv') as f:
    reader = csv.DictReader(f)
    # print(list(reader)[:5])
    for row in reader:
        # print(row)
        
        print(row)
        es.index(index='cv-transcriptions-4',
                document=row)
    # helpers.bulk(es, reader, index='cv-transcriptions')