import tushare as ts

from data.databasemgr import DatabaseMgr

result = ts.get_stock_basics()

print(result.loc['300325'])