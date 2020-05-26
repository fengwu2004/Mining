from data.securities import Securities
from data.codeInfo import CodeInfo
from storemgr.storemgr import SecuritiesMgr

def test():

    result:list[CodeInfo] = list()

    for securities in SecuritiesMgr.instance().securitiesList:

        lastIndex = len(securities.klines) - 1

        if lastIndex < 0:

            continue;

        if securities.toatlCapital() > 500 or securities.toatlCapital() < 50:

            continue

        if securities.touchHighServeralTimes():

            pass

        result.append(securities.codeInfo)



test()