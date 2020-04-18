from datetime import datetime

from data.securities import Securities
from data.klineModel import KLineModel
from data.databasemgr import DatabaseMgr
from typing import Dict
import tushare as ts

def loadAllStockFromDB() -> Dict[str, Securities]:

    result = dict()

    items = DatabaseMgr.instance().stocks.find({}, {'_id': 0})

    for item in items:

        if 'code' in item:

            print(item['code'])

            code = item['code']

            if code == 0:

                continue

            securities = Securities.fromJson(item)

            securities.calcMinsAndMaxs()

            result[code] = securities

    return result

_instance = None
class StockMgr(object):

    @classmethod
    def instance(cls):

        global _instance

        if _instance is None:

            _instance = StockMgr()

            _instance.loadStocks()

        return _instance

    def loadStocks(self):

        d = datetime.now().timestamp()

        self.date = datetime.now().strftime('%Y%m%d')

        self.securitiesList = loadAllStockFromDB()

        self.stockbasic = ts.get_stock_basics()

    def getStock(self, code:str) -> Securities:

        if code in self.stocks:

            return self.stocks[stockId]

        return None

    def __init__(self):

        self.securitiesList = None

        self.date = None

        self.stockbasic = None

        self.loadStocks()

    def getStockbasic(self, stockId:str):

        try:
            basic = self.stockbasic.loc[stockId]

            return basic

        except Exception:

            return None

def getStockName(code:str):

    stock = StockMgr.instance().getStock(code)

    if stock is not None:

        return stock.name

    return None

def getStockCode(name:str):

    items = DatabaseMgr.instance().stockInfos.find({'name': name}, {'_id': 0})

    results = []

    for item in items:
        
        return item['code']

    return None

loadAllStockFromDB()