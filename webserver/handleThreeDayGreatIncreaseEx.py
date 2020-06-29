import json
from webserver.RequestBaseManager import RequestBaseManager
from data.databasemgr import DatabaseMgr
from data.block import CodeInfo, BlockInfo
from data.codeInfo import CodeInfo
from storemgr.storemgr import SecuritiesMgr
from strategy.find_continue_increase import FindContinueIncrease
from strategy.find_hot_securities import FindHotSecurities


class HandleThreeDayGreatIncrease(RequestBaseManager):
    
    def post (self, *args, **kwargs):

        # data = json.loads(self.request.body.decode('utf-8'))

        result = list()

        codeInfos = FindHotSecurities.instance().getGreatIncreaseInDay(10, 0.2)

        for codeInfo in codeInfos:

            result.append(codeInfo.toJson())

        self.write({'success': 1, "data":{"codeInfos":result}})