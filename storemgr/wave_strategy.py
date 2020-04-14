# 策略:找到振幅到达alpha的第一个点，如果为+，则更高点进来，更新，低点如果达到-alpha的条件，则第一个高点确定，再来确定低点，更低点进来，更新，高点如果振幅达到alpha，则低点确定，再次寻找高点
class WaveStrategyUnit(object):
    
    def __init__(self, stock, alpha):
        
        self.maxs = []

        self.mins = []

        self.alpha = alpha

        self.id = stock.id
        
        self.lastday = 0
        
        self.name = stock.name

        self.calcMinsAndMaxs(stock)
        
    def calcMinsAndMaxs(self, stock):
    
        totals = stock.dayvalues
        
        if len(totals) <= 0:
            
            return

        self.lastday = totals[len(totals) - 1]
        
        i = 0

        dayvalue = totals[0]

        tempMin = dayvalue

        tempMax = dayvalue

        while i < len(totals) - 1:
    
            i = i + 1
    
            dayvalue = totals[i]
    
            if tempMax is not None and dayvalue.close < tempMax.close * (1 - self.alpha):
                
                self.maxs.append(tempMax)
        
                tempMax = None
        
                tempMin = dayvalue
        
                continue
    
            if tempMin is not None and dayvalue.close < tempMin.close:
                
                tempMin = dayvalue
        
                continue
    
            if tempMin is not None and dayvalue.close > tempMin.close * (1 + self.alpha):
                
                self.mins.append(tempMin)
        
                tempMin = None
        
                tempMax = dayvalue
        
                continue
    
            if tempMax is not None and dayvalue.close > tempMax.close:
                
                tempMax = dayvalue
        
                continue
        