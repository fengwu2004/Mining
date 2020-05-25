from data.securities import Securities
from storemgr.storemgr import SecuritiesMgr

def test():

    for securities in SecuritiesMgr.instance().securitiesList:

        if len(securities.klines) <= 0:

            continue;

        lastIndex = len(securities.klines) - 1

        totalCapital = securities.capital * securities.klines[lastIndex].close

        billion = 1000000000

        if totalCapital < 2 * billion or totalCapital > 50 * billion:

            continue

        securities.calcMinsAndMaxs()

        minsLen = len(securities.mins) - 1

        if len(securities.maxs) > 0 and len(securities.mins) > 0 and securities.klines[lastIndex].isHammer():

            print(securities.codeInfo.name)

test()