from data import storemgr
from pymongo import MongoClient

def run():

    stocks = loadFromDB()

    uri = "mongodb://yanli:9394@123.207.213.131:27017/recommond?authMechanism=SCRAM-SHA-1"

    client = MongoClient(uri)

    db = client["recommond"]
    
    collection = db['stockinfo']

    collection.remove({})
    
    result = []
    
    for stock in stocks:
    
        unit = dict()
        
        unit['id'] = stock.id
        
        unit['name'] = stock.name

        result.append(unit)

    collection.insert_many(result)
        
def test():
    
    client = MongoClient('localhost', 27017)
    
    db = client["test"]
    
    collection = db['stockinfo']
    
    result = []
    
    for i in range(100):
        
        unit = dict()
    
        unit['id'] = i
    
        unit['name'] = '广发银行'
        
        result.append(unit)

    collection.insert_many(result)
    
def add():
    
    stocks = storemgr.loadFromDB()
    
    uri = "mongodb://localhost:27017/recommond?authMechanism=SCRAM-SHA-1"
    
    client = MongoClient(uri)
    
    db = client['recommond']

    collection = db['stockinfo']

    result = []

    for stock in stocks:
        
        unit = dict()
    
        unit['id'] = stock.id
    
        unit['name'] = stock.name
    
        result.append(unit)

    collection.insert_many(result)