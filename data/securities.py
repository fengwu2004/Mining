import time
from data.klineModel import KLineModel
from data.codeInfo import CodeInfo
from typing import List

alpha = 0.18

class Securities(object):

    def __init__ (self):

        self.codeInfo:CodeInfo = None

        self.klines:List[KLineModel] = list()

        self.maxs = []

        self.mins = []

    def findIndex(self, date:int):

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

    def getCountOfLimitUp(self, beginDate:int) -> int:

        result = 0

        if len(self.klines) <= 0 or self.klines[0].date > beginDate:

            return 0

        for kline in self.klines:

            if kline.date < beginDate:

                continue

            if kline.preClose == 0:

                continue

            if (kline.close - kline.preClose)/kline.preClose > 0.095:

                result += 1
        
        return result

    def isNew(self) -> bool:

        return len(self.klines) < 200

    def findHeighestValue(self, date:int) -> KLineModel:

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
            'klines':klines
        }

    # 高点依次升高
    def increaseTrend(self):

        if len(self.maxs) < 2:

            return False

        return all([self.maxs[i].close < self.maxs[i + 1].close for i in range(len(self.maxs) - 1)]) and all([self.mins[i].close < self.mins[i + 1].close for i in range(len(self.mins) - 1)])

    def calcMinsAndMaxs(self):

        self.maxs = []

        self.mins = []

        totals = self.klines

        if len(totals) <= 0:

            return

        i = 0

        dayvalue = totals[0]

        tempMin = dayvalue

        tempMax = dayvalue

        while i < len(totals) - 1:

            i = i + 1

            dayvalue = totals[i]

            if tempMax is not None and dayvalue.close < tempMax.close * (1 - alpha):

                self.maxs.append(tempMax)

                tempMax = None

                tempMin = dayvalue

                continue

            if tempMin is not None and dayvalue.close < tempMin.close:

                tempMin = dayvalue

                continue

            if tempMin is not None and dayvalue.close > tempMin.close * (1 + alpha):

                self.mins.append(tempMin)

                tempMin = None

                tempMax = dayvalue

                continue

            if tempMax is not None and dayvalue.close > tempMax.close:

                tempMax = dayvalue

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

        for item in jsonvalue['klines']:

            obj.klines.append(KLineModel.fromJson(item))

        return obj