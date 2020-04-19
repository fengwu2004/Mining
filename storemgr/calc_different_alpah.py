from data.securities import Securities
from strategy.wave_strategy import WaveStrategyUnit
import jsonpickle
from pymongo import MongoClient
from strategy.strategy_find_increase import checkInAdjustWave

import json

alpha = 0.12

def loadFromDB ():
    
    stocks = []

    client = MongoClient('localhost', 27017)

    db = client["test"]

    coll = db['stocks']
    
    results = coll.find({}, {'_id': 0})
    
    for r in results:
        
        stocks.append(Securities.fromJson(r))
    
    return stocks

def load():
    
    stocks = loadFromDB()

    results = []
    
    global alpha
    
    for stock in stocks:
        
        wavaUnit = WaveStrategyUnit(stock, alpha)
        
        if checkInAdjustWave(wavaUnit):
        
            results.append(wavaUnit)
            
    return results

def save():
    
    results = load()
    
    client = MongoClient('localhost', 27017)
    
    db = client["test"]
    
    name = "alpha_increase_%s" % alpha
    
    coll = db[name]

    coll.remove({})
        
    v = json.loads(jsonpickle.encode(results))
    
    coll.insert_many(v)
    
def display():

    client = MongoClient('localhost', 27017)
    
    db = client["test"]
    
    name = "alpha_increase_%s" % alpha
    
    coll = db[name]
    
    items = coll.find({}, {'_id':0})
    
    for item in items:
        
        print(item['id'] + ' ' + item['name'])
        
save()

display()
