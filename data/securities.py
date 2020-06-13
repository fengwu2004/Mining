import time
from data.klineModel import KLineModel
from data.codeInfo import CodeInfo
from typing import List, Optional
import copy

alpha = 0.18

class Securities(object):

    def __init__ (self):

        self.codeInfo:Optional[CodeInfo] = None

        self.klines:List[KLineModel] = list()

        self.weekKLines: List[KLineModel] = list()

        self.capital = 0

        self.maxs:List[KLineModel] = list()

        self.mins:List[KLineModel] = list()

    def findIndex(self, date:int) -> int:

        index = 0

        for kline in self.klines:

            if kline.date == date:

                return index

            index += 1

        return -1

    def toatlCapital(self) -> float:

        lastIndex = len(self.klines) - 1

        if lastIndex < 0:

            return 0

        return self.klines[lastIndex].close * self.capital/100000000

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

    def getCountOfGreatIncrease(self, klineCount: int) -> int:

        result = 0

        if len(self.klines) <= klineCount:

            return 0

        for kline in self.klines[len(self.klines) - klineCount:]:

            if (kline.close - kline.preClose) / kline.preClose > 0.095:

                result += 1

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

    def isInDecrease(self, startIndex:int, endIndex:int) -> (bool, Optional[KLineModel], Optional[KLineModel]):

        if endIndex > len(self.klines) or startIndex < 0:

            return False, None, None

        maxIndex = -1

        maxvValue = -100000000

        minIndex = -1

        minValue = 100000000

        maxKLine = None

        minKLine = None

        for i in range(startIndex, endIndex):

            kLine = self.klines[i]

            if maxvValue < kLine.high:

                maxvValue = kLine.high

                maxIndex = i

                maxKLine = kLine

            if minValue > kLine.low:

                minValue = kLine.low

                minIndex = i

                minKLine = kLine

        if minIndex == -1 or maxIndex == -1:

            return False, None, None

        result = maxIndex < minIndex - 5 and (maxvValue - minValue) / minValue > 0.18

        return result, maxKLine, minKLine

    def isInIncrease(self, startIndex:int, endIndex:int, detal:float) -> (bool, Optional[KLineModel], Optional[KLineModel]):

        if endIndex > len(self.klines) or startIndex < 0:

            return False, None, None

        maxIndex = -1

        maxvValue = -100000000

        minIndex = -1

        minValue = 100000000

        maxKLine = None

        minKLine = None

        for i in range(startIndex, endIndex):

            kLine = self.klines[i]

            if maxvValue < kLine.high:

                maxvValue = kLine.high

                maxIndex = i

                maxKLine = kLine

            if minValue > kLine.low:

                minValue = kLine.low

                minIndex = i

                minKLine = kLine

        if minIndex == -1 or maxIndex == -1:

            return False, None, None

        result = minIndex < maxIndex - 5 and (maxvValue - minValue) / minValue > detal

        return result, maxKLine, minKLine

    def findVibrate(self) -> bool:

        totalLength = len(self.klines)

        inDecrease = self.isInDecrease(totalLength - 20, totalLength)

        if inDecrease[0] is False:

            return False

        maxKLine:KLineModel = inDecrease[1]

        inIncrease = self.isInIncrease(maxKLine.index - 30, maxKLine.index + 1, 0.18)

        if inIncrease[0] is False:

            return False

        if inIncrease[1].index != inDecrease[1].index:

            return  False

        return self.twoValueClose(inIncrease[2].low, inDecrease[1].low, 0.05)

    def twoValueClose(self, value1:float, value2:float, detal:float) -> bool:

        if value2 * (1 + detal) > value1 > (1 - detal) * value2:

            return True

        if value1 * (1 + detal) > value2 > (1 - detal) * value1:

            return True

        return False

    def findHigh(self, startIndex:int, endIndex:int) -> Optional[KLineModel]:

        result = None

        highValue = -1000000000

        for i in range(max(0, startIndex), min(endIndex, len(self.klines) - 1)):

            kLine = self.klines[i]

            if kLine.high > highValue:

                result = kLine

                highValue = kLine.high

        return result

    def findLow(self, startIndex:int, endIndex:int) -> Optional[KLineModel]:

        result = None

        lowValue = 1000000000

        for i in range(max(0, startIndex), min(endIndex, len(self.klines) - 1)):

            kLine = self.klines[i]

            if kLine.high < lowValue:

                result = kLine

                lowValue = kLine.high

        return result

    def touchHighServeralTimes(self) -> bool:

        lastIndex = len(self.klines) - 1

        high = self.findHigh(lastIndex - 10, lastIndex + 1)

        if high is None:

            return False

        temp = self.findHigh(high.index - 5, lastIndex + 1)

        if temp.index != high.index:

            return False

        interval = 5

        times = self.touchHighValueTimes(high, interval)

        if times <= 2:

            return False

        low = self.findLow(high.index - interval, lastIndex + 1)

        if low is None:

            return False

        if (high.high - low.low)/low.low < 0.15:

            return False

        print(high.date, low.date, times, self.codeInfo.name)

        return True

    # 高点依次升高，低点依次升高，同时高点比低点高
    def inInIncreaseWave(self) -> bool:

        if len(self.mins) <= 0:

            return True


    def touchHighValueTimes(self, kLine:KLineModel, interval:int) -> int:

        highValue = kLine.high

        count = 0

        for i in range(kLine.index - interval, kLine.index):

            if i < 0 or i >= len(self.klines):

                break

            if self.twoValueClose(highValue, self.klines[i].high, 0.02):

                count += 1

        for i in range(kLine.index + 1, kLine.index + interval):

            if i < 0 or i >= len(self.klines):

                break

            if self.twoValueClose(highValue, self.klines[i].high, 0.02):

                count += 1

        return count

    def isSTIB(self):

        if "688" not in self.codeInfo.name:

            return False

        if self.codeInfo.code.index("688") == 0:

            return True

        return False

    def isST(self):

        if "ST" in self.codeInfo.name:

            return True

        return False

    def checkFindMaxFirst(self, kLines:List[KLineModel]) -> bool:

        i = 0

        tempMin = kLines[0]

        tempMax = kLines[0]

        print(tempMax.date)

        while i < len(kLines) - 1:

            i = i + 1

            kLine = kLines[i]

            if tempMin.close > kLine.close:

                tempMin = kLine

            if tempMax.close < kLine.close:

                tempMax = kLine

            if tempMax.date > tempMin.date and tempMax.close > tempMin.close * (1 + alpha):

                return False

        return True

    def calcMinsAndMaxs(self):

        self.maxs = []

        self.mins = []

        if len(self.klines) < 200:

            return

        kLines = self.klines[-200:]

        findMaxFirst = self.checkFindMaxFirst(kLines)

        while len(kLines) > 0:

            if findMaxFirst:

                tempMax = self.findMax(kLines)

                if tempMax:

                    self.maxs.append(tempMax)

                tempMin = self.findMin(kLines)

                if tempMin:

                    self.mins.append(tempMin)

            else:

                tempMin = self.findMin(kLines)

                if tempMin:

                    self.mins.append(tempMin)

                tempMax = self.findMax(kLines)

                if tempMax:

                    self.maxs.append(tempMax)

        [print(x.close, x.date) for x in self.mins]

        print("--------")

        [print(x.close, x.date) for x in self.maxs]

    def findMin(self, kLines:List[KLineModel]):

        if len(kLines) == 0:

            return None

        kLine = kLines[0]

        tempMin = kLine

        tempMax = kLine

        del kLines[0]

        while len(kLines) > 0:

            kLine = kLines[0]

            del kLines[0]

            if tempMax.date > tempMin.date and tempMax.close > tempMin.close * (1 + alpha):

                break

            if kLine.close < tempMin.close:

                tempMin = kLine

                tempMax = kLine

            if kLine.close > tempMax.close:

                tempMax = kLine

        return tempMin

    def findMax(self, kLines:List[KLineModel]):

        if len(kLines) == 0:

            return None

        kLine = kLines[0]

        tempMin = kLine

        tempMax = kLine

        del kLines[0]

        while len(kLines) > 0:

            kLine = kLines[0]

            del kLines[0]

            if tempMin.date > tempMax.date and tempMax.close > tempMin.close * (1 + alpha):

                break

            if kLine.close < tempMin.close:

                tempMin = kLine

            if kLine.close > tempMax.close:

                tempMax = kLine

                tempMin = kLine

        return tempMax

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