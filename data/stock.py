import time
from data.klineModel import KLineModel

alpha = 0.18

class Securities(object):

    def __init__ (self):

        self.id = 0

        self.name = ''

        self.klines = []

        self.maxs = []

        self.mins = []

    def findIndex(self, date:str):

        t0 = time.strptime(date, '%Y/%m/%d')

        index = 0

        for kline in self.klines:

            t = time.strptime(kline.date, '%Y/%m/%d')

            if t < t0:

                index += 1
            else:

                break

        return index

    def isNew(self) -> bool:

        return len(self.klines) < 45

    def findHeighestValue(self, date:str) -> KLineModel:

        start = self.findIndex(date)

        if start >= len(self.klines):

            return None

        return max(self.klines[start:], key = lambda x: x.close)

    def findLowestValue(self, date:str) -> KLineModel:

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

    def getDayIndex(self, date:str):

        t0 = time.strptime(date, '%Y/%m/%d')

        index = 0

        for dayvalue in self.klines:

            t = time.strptime(dayvalue.date, '%Y/%m/%d')

            if t < t0:

                index += 1
            else:
                break

        return index

    def toJson(self):

        dayvalues = []

        for dayvalue in self.klines:

            dayvalues.append(dayvalue.toJson())

        return {
            'id':self.id,
            'name':self.name,
            'dayvalues':dayvalues
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

        obj.id = jsonvalue['id']

        obj.name = jsonvalue['name']

        obj.dayvalues = []

        for item in jsonvalue['dayvalues']:

            obj.klines.append(KLineModel.fromJson(item))

        return obj