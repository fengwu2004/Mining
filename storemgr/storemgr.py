from datetime import datetime

from data.securities import Securities
from data.klineModel import KLineModel
from data.databasemgr import DatabaseMgr
from data.codeInfo import CodeInfo
from data.block import BlockInfo
from typing import Dict, List
import tushare as ts

def loadAllSecuritiesFromDB() -> List[Securities]:

    result:List[Securities] = []

    items = DatabaseMgr.instance().stocks.find({}, {'_id': 0})

    for item in items:

        if 'code' in item:

            code = item['code']

            if code == 0:

                continue

            securities = Securities.fromJson(item)

            securities.calcMinsAndMaxs()

            result.append(securities)

    return result

def loadAllBlockFromDB() -> List[BlockInfo]:
    
    result:List[BlockInfo] = []

    items = DatabaseMgr.instance().block.find({}, {'_id': 0})

    for item in items:

        if 'name' in item and "codeList" in item:

            name = item['name']

            codeList = item['codeList']

            if name is None:

                continue

            blockInfo = BlockInfo()

            blockInfo.createFromJson(name, codeList)

            result.append(blockInfo)

    return result

_instance = None
class SecuritiesMgr(object):

    @classmethod
    def instance(cls):

        global _instance

        if _instance is None:

            _instance = SecuritiesMgr()

            _instance.loadSecuritiess()

        return _instance

    def __init__(self):
    
        self.securitiesList:List[Securities] = None

        self.blockList:List[BlockInfo] = None

        self.date = None

        self.stockbasic = None

        self.loadSecuritiess()

        super().__init__()

    def loadSecuritiess(self):

        d = datetime.now().timestamp()

        self.date = datetime.now().strftime('%Y%m%d')

        self.securitiesList = loadAllSecuritiesFromDB()

        self.blockList = loadAllBlockFromDB();

        self.stockbasic = ts.get_stock_basics()

    def getSecurities(self, codeInfo:CodeInfo) -> Securities:

        for securities in self.securitiesList:

            if securities.codeInfo == codeInfo:

                return securities

        return None

loadAllBlockFromDB()