import json
from webserver.RequestBaseManager import RequestBaseManager
from data.databasemgr import DatabaseMgr
from data.block import CodeInfo, BlockInfo
from data.codeInfo import CodeInfo
from storemgr.storemgr import SecuritiesMgr
from strategy.find_continue_increase import FindContinueIncrease

def findRightPe():

    result:list[CodeInfo] = list()

    for securities in SecuritiesMgr.instance().securitiesList:

        if len(securities.klines) < 200:

            continue

        lastIndex = len(securities.klines) - 1

        if securities.isST():

            continue

        if securities.toatlCapital() > 150 or securities.toatlCapital() < 40:

            continue

        result.append(securities.codeInfo)

    return result


class HandleRightPE(RequestBaseManager):
    
    def post (self, *args, **kwargs):

        # data = json.loads(self.request.body.decode('utf-8'))
        
        codeInfos = findRightPe()

        result = list()

        for codeInfo in codeInfos:

            result.append(codeInfo.toJson())

        self.write({'success': 1, "data":{"codeInfos":result}})