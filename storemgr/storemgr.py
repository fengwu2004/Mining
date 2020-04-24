from datetime import datetime

from data.securities import Securities
from data.klineModel import KLineModel
from data.databasemgr import DatabaseMgr
from data.codeInfo import CodeInfo
from data.block import BlockInfo
from typing import Dict, List
import tushare as ts

abortBlocks = {
    "送转预期",
    "富时概念",
    "创业成份",
    "MSCI中国",
    "HS300",
    "基金重仓",
    "MSCI大盘",
    "股权激励",
    "中字头",
    "创业板综",
    "上证180",
    "标普概念",
    "昨日涨停",
    "深成500",
    "创投",
    "深成500",
    "京津冀",
    "证金持股",
    "创业板壳",
    "IPO受益", 
    "长江三角",
    "举牌概念",
    "沪股通", 
    "中证500",
    "壳资源",
    "MSCI中盘",
    "虚拟现实",
    "预盈预增",
    "共享经济",
    "深圳特区",
    "高送转", "上证380", "转债标的", "融资融券", "贬值受益", "昨日连板", "分拆预期", "机构重仓", "ST概念", "深股通", "债转股", "AH股", "AB股", "创业板壳"}

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

            if name is None or name in abortBlocks:

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