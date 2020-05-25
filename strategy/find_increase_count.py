from data.securities import Securities
from data.codeInfo import CodeInfo
from data.block import BlockInfo
from storemgr.storemgr import SecuritiesMgr
from typing import Dict, List
from storemgr.excel_mananger import ExcelMgr
import datetime

def findIncreaseCount():

    inHighRange:List[Securities] = []

    inLowRange:List[Securities] = []

    securitiesList = SecuritiesMgr.instance().securitiesList

    for securities in securitiesList:

        result = securities.isInEdgeRange()

        lastIndex = len(securities.klines) - 1

        if result[0] is True and 20000000000 < securities.capital * securities.klines[lastIndex].close < 35000000000:

            inHighRange.append(securities)

        if result[1] is True and 5000000000 > securities.capital * securities.klines[lastIndex].close > 2000000000:

            inLowRange.append(securities)

    print("在低位的股票数目为 " + str(len(inLowRange)))

    for item in inLowRange:

        print(item.codeInfo.name)

findIncreaseCount()