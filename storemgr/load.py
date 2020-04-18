import time
from data.stock import Securities, KLineModel

def getLines(file):

    lines = [line.rstrip('\n') for line in open(file, 'r+', encoding='gbk')]

    lines.pop(1)

    lines.pop()
    
    return lines

def getTime(value):
    
    return time.strptime(value, '%Y/%m/%d')

def formatData(lines):
    
    stock = Securities()
    
    if len(lines) > 1:
        
        values = lines[0].split(' ')
        
        stock.id = values[0]
        
        i = 1
        
        while values[i] != '日线':
        
            stock.name += values[i]
            
            i += 1
        
        lines.pop(0)

    if len(lines) <= 1:
        
        return stock
    
    for line in lines:
        
        dayvalue = KLineModel()
    
        values = line.split('\t')

        if getTime(values[0]) < time.strptime('2017/1/01', '%Y/%m/%d'):
            
            continue

        dayvalue.date = values[0]

        dayvalue.open = float(values[1])

        dayvalue.high = float(values[2])

        dayvalue.low = float(values[3])

        dayvalue.close = float(values[4])

        dayvalue.tradeamount = float(values[5])

        dayvalue.tradevolume = float(values[6])

        stock.klines.append(dayvalue)
        
    return stock