import time
from data.klineModel import KLineModel
from data.codeInfo import CodeInfo
from typing import List, Optional

alpha = 0.18

class Securities(object):

    def __init__ (self):

        self.codeInfo:Optional[CodeInfo] = None

        self.klines:List[KLineModel] = list()

        self.capital = 0

        self.maxs:List[KLineModel] = list()

        self.mins:List[KLineModel] = list()

    def findIndex(self, date:int) -> int:

        index = 0

        for kline in self.klines:

            if kline.date == date:

                return index

            ++index

        return -1

    def doSomeTest(self, beginDate:int):

        for kline in self.klines:
    
            if kline.date < beginDate:

                continue

            if kline.preClose == 0:

                continue

            if (kline.close - kline.preClose)/kline.preClose > 0.095:

                print(kline.date)

    def getContinueIncreateUntil(self, endDate:int) -> int:

        result = 0

        count = len(self.klines)

        if count <= 200:

            return 0

        for kline in reversed(self.klines):

            if kline.date > endDate:

                continue

            if kline.preClose == 0:

                continue

            if (kline.close - kline.preClose)/kline.preClose > 0.095:

                result += 1
            
            else:

                break
        
        return result

    def getCountOfLimitUp(self, beginDate:int, endDate:int) -> int:
    
        result = 0

        if len(self.klines) <= 0 or self.klines[0].date > beginDate:

            return 0

        for kline in self.klines:

            if kline.date < beginDate or kline.date > endDate:

                continue

            if kline.preClose == 0:

                continue

            if (kline.close - kline.preClose)/kline.preClose > 0.095:

                result += 1
        
        return result

    def isNew(self) -> bool:

        return len(self.klines) < 200

    def findHeighestValue(self, date:int) -> Optional[KLineModel]:

        start = self.findIndex(date)

        if start < len(self.klines):

            return None

        return max(self.klines[start:], key = lambda x: x.close)

    def findLowestValue(self, date:int) -> KLineModel:

        start = self.findIndex(date)

        if start >= len(self.klines):

            return None

        return min(self.klines[start:], key = lambda x: x.low)

    def getDayValue(self, index:int) -> KLineModel:

        if index < 0:

            return self.klines[0]

        if index >= len(self.klines):

            return self.klines[len(self.klines) - 1]

        return self.klines[index]

    def getDayIndex(self, date:int) -> int:

        index = 0

        for kline in self.klines:

            if kline.date == date:

                return index

            ++index

        return index

    def toJson(self):
    
        klines = []

        for kline in self.klines:

            klines.append(kline.toJson())

        return {
            'codeInfo':self.codeInfo.toJson(),
            'klines':klines,
            "capitalization":self.capitalization
        }

    # 高点依次升高,处于上升趋势
    def increaseTrend(self):

        if len(self.maxs) < 2:

            return False

        return all([self.maxs[i].close < self.maxs[i + 1].close for i in range(len(self.maxs) - 1)]) and all([self.mins[i].close < self.mins[i + 1].close for i in range(len(self.mins) - 1)])

    def isInEdgeRange(self) -> (bool, bool):

        maxValue = 0

        if len(self.klines) < 200:

            return False, False

        closePrices = [x.close for x in self.klines]

        maxValue = max(closePrices)

        minValue = min(closePrices)

        lastIndex = len(self.klines) - 1

        return self.klines[lastIndex].close > 0.85 * maxValue, self.klines[lastIndex].close < minValue/0.85

    def calcMinsAndMaxs(self):

        self.maxs = []

        self.mins = []

        kLines = self.klines

        if len(kLines) <= 0:

            return

        i = 0

        KLine = kLines[0]

        tempMin = KLine

        tempMax = KLine

        while i < len(kLines) - 1:

            i = i + 1

            KLine = kLines[i]

            if tempMax is not None and KLine.close < tempMax.close * (1 - alpha):

                self.maxs.append(tempMax)

                tempMax = None

                tempMin = KLine

                continue

            if tempMin is not None and KLine.close < tempMin.close:

                tempMin = KLine

                continue

            if tempMin is not None and KLine.close > tempMin.close * (1 + alpha):

                self.mins.append(tempMin)

                tempMin = None

                tempMax = KLine

                continue

            if tempMax is not None and KLine.close > tempMax.close:

                tempMax = KLine

                continue

    @classmethod
    def fromJson(cls, jsonvalue):

        if jsonvalue is None:

            return None

        obj = Securities()

        obj.codeInfo = CodeInfo()
        
        obj.codeInfo.name = jsonvalue['name']

        obj.codeInfo.code = jsonvalue['code']

        obj.klines = []

        index = 0

        for item in jsonvalue['klines']:

            kLine = KLineModel.fromJson(item)

            kLine.index = index

            index += 1

            obj.klines.append(kLine)

        return obj