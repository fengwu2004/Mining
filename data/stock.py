import time
alpha = 0.18
class DayValue(object):

    def __init__(self):

        self.open = 0

        self.close = 0

        self.low = 0

        self.high = 0

        self.date = ''

        self.tradeamount = 0

        self.tradevolume = 0

    def isHammer(self):

        return self.isHammer_green() or self.isHammer_red()

    def isHammer_red(self):

        if self.close < self.open:

            return False

        if (self.high - self.low)/self.open < 0.06:

            return False

        if self.open - self.close != 0 and (self.open - self.low)/(self.close - self.open) < 2:

            return False

        if (self.high - self.open)/(self.high - self.low) > 0.33:

            return False

        return True

    def isHammer_green(self):

        if self.open < self.close:

            return False

        if (self.high - self.low)/self.open < 0.06:

            return False

        if self.open - self.close != 0 and (self.close - self.low)/(self.open - self.close) < 2:

            return False

        if (self.high - self.close) / (self.high - self.low) > 0.33:

            return False

        return True

    def toJson(self):

        return {
            'Open':self.open,
            'Close':self.close,
            'Low': self.low,
            'High': self.high,
            'Date': self.date,
            'tradeamount': self.tradeamount,
            'Volume': self.tradevolume,
        }

    @classmethod
    def fromJson(cls, jsonvalue):

        obj = DayValue()

        obj.open = jsonvalue['Open']

        obj.close = jsonvalue['Close']

        obj.low = jsonvalue['Low']

        obj.high = jsonvalue['High']

        obj.date = jsonvalue['Date']

        obj.tradeamount = jsonvalue['tradeamount']

        obj.tradevolume = jsonvalue['Volume']

        return obj

class Stock(object):

    def __init__ (self):

        self.id = 0

        self.name = ''

        self.dayvalues = []

        self.maxs = []

        self.mins = []

    def findIndex(self, date:str):

        t0 = time.strptime(date, '%Y/%m/%d')

        index = 0

        for dayvalue in self.dayvalues:

            t = time.strptime(dayvalue.date, '%Y/%m/%d')

            if t < t0:

                index += 1
            else:

                break

        return index

    def isNew(self) -> bool:

        return len(self.dayvalues) < 45

    def findHeighestValue(self, date:str) -> DayValue:

        start = self.findIndex(date)

        if start >= len(self.dayvalues):

            return None

        return max(self.dayvalues[start:], key = lambda x: x.close)

    def findLowestValue(self, date:str) -> DayValue:

        start = self.findIndex(date)

        if start >= len(self.dayvalues):

            return None

        return min(self.dayvalues[start:], key = lambda x: x.low)

    def getDayValue(self, index:int) -> DayValue:

        if index < 0:

            return self.dayvalues[0]

        if index >= len(self.dayvalues):

            return self.dayvalues[len(self.dayvalues) - 1]

        return self.dayvalues[index]

    def getDayIndex(self, date:str):

        t0 = time.strptime(date, '%Y/%m/%d')

        index = 0

        for dayvalue in self.dayvalues:

            t = time.strptime(dayvalue.date, '%Y/%m/%d')

            if t < t0:

                index += 1
            else:
                break

        return index

    def toJson(self):

        dayvalues = []

        for dayvalue in self.dayvalues:

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

        totals = self.dayvalues

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

        obj = Stock()

        obj.id = jsonvalue['id']

        obj.name = jsonvalue['name']

        obj.dayvalues = []

        for item in jsonvalue['dayvalues']:

            obj.dayvalues.append(DayValue.fromJson(item))

        return obj