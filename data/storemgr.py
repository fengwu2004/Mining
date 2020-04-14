from datetime import datetime

from data.stock import Stock, DayValue
from data.suggest import Suggest, Consultor, SuggestScore
from data.databasemgr import DatabaseMgr
from typing import Dict

from data.suggest_manager import SuggestMgr
import tushare as ts

def loadAllStockFromDB() -> Dict[str, Stock]:
    stocks = dict()

    items = DatabaseMgr.instance().stocks.find({}, {'_id': 0})

    for item in items:

        if 'id' in item:

            print(item['id'])

            stockId = item['id']

            stock = Stock.fromJson(item)

            stock.calcMinsAndMaxs()

            stocks[stockId] = stock

    return stocks

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

        self.date = datetime.now().strftime('%Y/%m/%d')

        # print('begin load stocks')

        self.stocks = loadAllStockFromDB()

        # print('load stocks finish')

        # print(datetime.now().timestamp() - d)

        self.stockbasic = ts.get_stock_basics()

    def checkIsLowVolatility(self, stockId:str) -> bool:

        stock = self.getStock(stockId)

        valuemax = stock.findHeighestValue('2017/1/1')

        if valuemax is None:

            return False

        valuemin = stock.findLowestValue(valuemax.date)

        if valuemin.isHammer() is not True:

            return False

        if valuemin is None:

            return False

        value = stock.findHeighestValue(valuemin.date)

        if value is None:

            return False

        return (value.high - valuemin.low) / valuemin.open < 0.15


    def checkIsSelfSelect(self, stockId:str) -> bool:

        items = DatabaseMgr.instance().selfselect.find({"stockid":stockId}, {'_id':0})

        for item in items:

            return True

        return False

    def getStock(self, stockId:str) -> Stock:

        if stockId in self.stocks:

            return self.stocks[stockId]

        return None

    def __init__(self):

        self.stocks = None

        self.date = None

        self.stockbasic = None

        self.loadStocks()

    def getStockbasic(self, stockId:str):

        try:
            basic = self.stockbasic.loc[stockId]

            return basic

        except Exception:

            return None

    def getIndustryStocks(self, industry:str):

        items = DatabaseMgr.instance().industry.find({'firstindustry':industry}, {'_id':0})

        stocks = None

        for item in items:

            stocks = list(item['stocks'])

        return stocks

def getStockLevel(stockId:str) -> int:

    items = DatabaseMgr.instance().stockLevels.find({'id':stockId})

    for item in items:

        return item['level']

    return -1

def checkUser(name, pwd):
    
    user = DatabaseMgr.instance().users.find({'name': name})
    
    for u in user:
        
        if u['pwd'] == pwd:
            
            return True
    
    return False

def getStock(stockId:str) -> Stock:

    return StockMgr.instance().getStock(stockId)

def getStockDayvalue(stockId:str, day:str) -> DayValue:

    stock = getStock(stockId)

    index = stock.getDayIndex(day)

    return stock.getDayValue(index - 1)

def getStockName(stockId:str):

    stock = StockMgr.instance().getStock(stockId)

    if stock is not None:

        return stock.name

    return None

def getStockId(name:str):

    items = DatabaseMgr.instance().stockInfos.find({'name': name}, {'_id': 0})

    results = []

    for item in items:
        
        return item['id']

    return None

def checkIsNewStock(stockId, dtstr:str):

    stock = getStock(stockId)

    if stock is None:

        return True

    index = stock.getDayIndex(dtstr)

    if index <= 10:

        return True

    return False
        