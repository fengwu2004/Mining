from data.securities import Securities
from data.codeInfo import CodeInfo
from data.block import BlockInfo
from storemgr.storemgr import SecuritiesMgr
from typing import Dict, List
from storemgr.excel_mananger import ExcelMgr
import datetime

_instance = None


class FindHotSecurities(object):

    @classmethod
    def instance(cls):

        global _instance

        if _instance is None:

            _instance = FindHotSecurities()

        return _instance

    def __init__(self):

        super().__init__()

        self.limitCount = 3

        self.day = 15

    def refreshHotSecurities(self):

        result: Dict[str, List[CodeInfo]] = dict()

        blockList = SecuritiesMgr.instance().blockList

        for block in blockList:

            for codeInfo in block.codeList:

                securities = SecuritiesMgr.instance().getSecurities(codeInfo)

                if securities is None or len(securities.klines) < 200:

                    continue

                count = securities.getCountOfGreatIncrease(self.day)

                if count < self.limitCount:

                    continue

                if result.get(block.name) is None:

                    result[block.name] = []

                result[block.name].append(codeInfo)

        self.storeToExcel(result)

    def getHotSecuritiesEx(self) -> List[CodeInfo]:

        result: List[CodeInfo] = list()

        for securities in SecuritiesMgr.instance().securitiesList:

            if len(securities.klines) < 150:

                continue

            lastkLine = securities.klines[len(securities.klines) - 1]

            count = securities.getCountOfGreatIncrease(self.day)

            if count != self.limitCount:

                continue

            result.append(securities.codeInfo)

        return result

    def getHotSecurities(self) -> List[CodeInfo]:

        result:List[CodeInfo] = list()

        for securities in SecuritiesMgr.instance().securitiesList:

            if len(securities.klines) < 200:

                continue

            lastkLine = securities.klines[len(securities.klines) - 1]

            count = securities.getCountOfGreatIncrease(self.day)

            if count < self.limitCount:

                continue

            result.append(securities.codeInfo)

        return result

    def storeToExcel(self, dic: Dict[str, List[CodeInfo]]):

        excelMgr = ExcelMgr()

        for key in dic:

            values = [codeInfo.name for codeInfo in dic[key]]

            excelMgr.saveRow(title=key, values=values)

        name = "/Users/aliasyan/OneDrive/mining/hot_block/hot_securities_great_increase_in_last_{0}_day_{1}_time_increase.xlsx".format(self.day, self.limitCount)

        excelMgr.save(name)


FindHotSecurities.instance().refreshHotSecurities()

print(FindHotSecurities.instance().limitCount, "finish")