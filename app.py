import time
from datetime import datetime
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://mongohost:27017/')
db = client['mydatabase']
collection = db['hits']

def get_hit_count():
    retries = 5
    while True:
        try:
            timestamp = datetime.utcnow()
            collection.insert_one({'timestamp': timestamp})
            return collection.count_documents({})
        except Exception as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)