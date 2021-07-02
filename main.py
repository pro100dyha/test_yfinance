import json
import yfinance as yf
from pymongo import MongoClient
from fastapi import FastAPI, Query

# Create the client
client = MongoClient('mongo', 27017)
# Connect to our database
db = client['SeriesDB']
# Fetch our series collection
series_collection = db['series']

app = FastAPI()
LIST_OF_COMPANIES = ['PD', 'ZUO', 'PINS', 'ZM', 'PVTL', 'DOCU', 'CLDR', 'RUN']


@app.on_event("startup")
async def startup_event():
    for company in LIST_OF_COMPANIES:
        msft = yf.Ticker(company)
        hist = msft.history(period="1day")
        result = hist.to_json(orient='table')
        json_data = json.loads(result)
        new_show = {
            "_id": company,
            "name": json_data['data']
        }
        try:
            if series_collection.find_one({'_id': company})['_id'] == company:
                series_collection.update_one({"_id": company}, {'$set': {'name': json_data['data']}})
        except TypeError:
            series_collection.insert_one(new_show)


@app.get('/get_statistics')
async def get_statistics(_q: str = Query("PD", enum=LIST_OF_COMPANIES)):
    return {_q: series_collection.find_one({'_id': _q})}
