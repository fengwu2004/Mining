import json
from webserver.RequestBaseManager import RequestBaseManager
from data.databasemgr import DatabaseMgr
from data.block import CodeInfo, BlockInfo
from data.codeInfo import CodeInfo
from storemgr.storemgr import SecuritiesMgr
from strategy.find_continue_increase import FindContinueIncrease


class HandleTotalSecurities(RequestBaseManager):
    
    def post (self, *args, **kwargs):

        data = json.loads(self.request.body.decode('utf-8'))

        result = list()

        count = int(data["count"])

        startIndex = int(data["startIndex"])

        print(startIndex, count)

        for securities in SecuritiesMgr.instance().securitiesList[startIndex:startIndex + count]:

            result.append(securities.toJson())

        self.write({'success': 1, "data":{"securities":result}})