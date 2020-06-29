import json
from data.databasemgr import DatabaseMgr
from data.block import CodeInfo, BlockInfo
from data.codeInfo import CodeInfo
from storemgr.storemgr import SecuritiesMgr
from strategy.find_hot_securities import FindHotSecurities

FindHotSecurities.instance().limitCount = 3

FindHotSecurities.instance().day = 15

FindHotSecurities.instance().endDate = 20200531

result = FindHotSecurities.instance().getHotSecurities()

list1 = [x.name for x in result]

FindHotSecurities.instance().limitCount = 2

FindHotSecurities.instance().day = 10

result = FindHotSecurities.instance().getHotSecuritiesEx()

list2 = [x.name for x in result]

result = FindHotSecurities.instance().getGreatIncreaseInDay(10, 0.2)

list3 = [x.name for x in result]

result = list1 + list2 + list3

result = list(set(result))

[print(x) for x in result]

