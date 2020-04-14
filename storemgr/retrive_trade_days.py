from datetime import datetime, timedelta
import time

holidays = [
    '2017/01/01',
    '2017/01/02',
    '2017/01/27',
    '2017/01/28',
    '2017/01/29',
    '2017/01/30',
    '2017/01/31',
    '2017/02/01',
    '2017/02/02',
    '2017/04/02',
    '2017/04/03',
    '2017/04/04',
    '2017/04/29',
    '2017/04/30',
    '2017/05/01',
    '2017/05/28',
    '2017/05/29',
    '2017/05/30',
    '2017/10/01',
    '2017/10/02',
    '2017/10/03',
    '2017/10/04',
    '2017/10/05',
    '2017/10/06',
    '2017/10/07',
    '2017/10/08',
    '2018/01/01',
    '2018/02/15',
    '2018/02/16',
    '2018/02/17',
    '2018/02/18',
    '2018/02/19',
    '2018/02/20',
    '2018/02/21',
    '2018/04/05',
    '2018/04/06',
    '2018/04/07',
    '2018/04/29',
    '2018/04/30',
    '2018/05/01',
    '2018/06/18',
    '2018/09/24',
    '2018/10/01',
    '2018/10/02',
    '2018/10/03',
    '2018/10/04',
    '2018/10/05',
    '2018/10/06',
    '2018/10/07',
    ]

def dt2t(dt:datetime)->time.struct_time:
    
    timestr = dt.strftime('%Y/%m/%d')
    
    return time.strptime(timestr, '%Y/%m/%d')

# time to datatime
def t2dt(t:time.struct_time) -> datetime:
    
    return datetime(t.tm_year, t.tm_mon, t.tm_mday)

#  is holiday of 2017(include weekend)
def isHolidays(dt:datetime) -> bool:
    
    if dt.weekday() == 5 or dt.weekday() == 6:
    
        return True
    
    timestr = dt.strftime('%Y/%m/%d')
    
    for item in holidays:
    
        if timestr == item:
            
            return True
        
    return False

def getPreTradeDay(date:str) -> datetime:

    dt = datetime.strptime(date, '%Y/%m/%d')

    dt = dt - timedelta(days = 1)

    while isHolidays(dt):

        dt = dt - timedelta(days = 1)

    if dt > datetime.now():

        return None

    return dt

def getNextTradeDay(date:str) -> datetime:
    
    dt = datetime.strptime(date, '%Y/%m/%d')

    dt = dt + timedelta(days = 1)

    while isHolidays(dt):
    
        dt = dt + timedelta(days = 1)
        
    if dt > datetime.now():
        
        return None

    return dt

def getTradeDayCount(dt1:datetime, dt2:datetime) -> int:

    days = (dt2 - dt1).days

    dt = dt1 + timedelta(days = 1)

    count = 0

    while days > 0:

        days -= 1

        if isHolidays(dt) is not True:

            count += 1

        dt = dt + timedelta(days = 1)

    return count

# test
def test():

    dt1 = datetime.strptime('2017/10/1', '%Y/%m/%d' )

    dt2 = datetime.strptime('2017/10/16', '%Y/%m/%d')

    d = getTradeDayCount(dt1, dt2)

    print(d)
    
    print(getPreTradeDay('2017/10/2'))
    
test()