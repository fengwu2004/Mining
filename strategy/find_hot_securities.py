from data.securities import Securities
from data.codeInfo import CodeInfo
from data.klineModel import KLineModel
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

        self.endDate = 99999999

    def reset(self):

        self.limitCount = 3

        self.day = 15

        self.endDate = 99999999

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

            if securities.isSTIB() or securities.isST():

                continue

            kLines = self.findKLines(securities.klines)

            if len(kLines) < 200:

                continue

            if kLines[len(kLines) - 1].close < 4:

                continue

            count = self.getCountOfGreatIncrease(self.day, kLines)

            if count != self.limitCount:

                continue

            if kLines[len(kLines) - 1].greateChangeRatio():

                continue

            result.append(securities.codeInfo)

        return result

    def findKLines(self, kLines:List[KLineModel]) -> List[KLineModel]:

        result:List[KLineModel] = list()

        for kLine in kLines:

            if kLine.date <= self.endDate:

                result.append(kLine)

        return result

    def getGreatIncreaseInDay(self, klineCount:int, increase:float) -> List[CodeInfo]:

        result: List[CodeInfo] = list()

        for securities in SecuritiesMgr.instance().securitiesList:

            if securities.isSTIB() or securities.isST():

                continue

            kLines = self.findKLines(securities.klines)

            if len(kLines) < 200:

                continue

            if kLines[len(kLines) - 1].close < 4:

                continue

            if kLines[len(kLines) - 1].greateChangeRatio():

                continue

            for i in range(len(kLines) - klineCount, len(kLines) - 3):

                if (kLines[i + 3].close - kLines[i].preClose) / kLines[i].preClose > increase:

                    result.append(securities.codeInfo)

                    break

        return result

    def getCountOfGreatIncrease(self, klineCount: int, kLines:List[KLineModel]) -> int:

        result = 0

        if len(kLines) <= klineCount:

            return 0

        for kline in kLines[len(kLines) - klineCount:]:

            if (kline.close - kline.preClose) / kline.preClose > 0.095:

                result += 1

        return result

    def getHotSecurities(self) -> List[CodeInfo]:

        result:List[CodeInfo] = list()

        for securities in SecuritiesMgr.instance().securitiesList:

            if securities.isSTIB() or securities.isST():

                continue

            kLines = self.findKLines(securities.klines)

            if len(kLines) < 200:

                continue

            if kLines[len(kLines) - 1].close < 4:

                continue

            count = self.getCountOfGreatIncrease(self.day, kLines)

            if count < self.limitCount:

                continue

            if kLines[len(kLines) - 1].greateChangeRatio():

                continue

            result.append(securities.codeInfo)

        return result

    def getGreatIncreaseInThreeDay(self) -> List[CodeInfo]:

        result:List[CodeInfo] = list()

        for securities in SecuritiesMgr.instance().securitiesList:

            if len(securities.klines) < 200:

                continue

            lastkLine = securities.klines[len(securities.klines) - 1]

            if securities.checkGreatIncreaseInDay(10, 0.20):

                result.append(securities.codeInfo)

        return result

    def storeToExcel(self, dic: Dict[str, List[CodeInfo]]):

        excelMgr = ExcelMgr()

        for key in dic:

            values = [codeInfo.name for codeInfo in dic[key]]

            excelMgr.saveRow(title=key, values=values)

        name = "/Users/aliasyan/OneDrive/mining/hot_block/hot_securities_great_increase_in_last_{0}_day_{1}_time_increase.xlsx".format(self.day, self.limitCount)

        excelMgr.save(name)


# FindHotSecurities.instance().refreshHotSecurities()
#
# print(FindHotSecurities.instance().limitCount, "finish")