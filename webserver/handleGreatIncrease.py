import json
from webserver.RequestBaseManager import RequestBaseManager
from data.databasemgr import DatabaseMgr
from data.block import CodeInfo, BlockInfo
from data.codeInfo import CodeInfo
from storemgr.storemgr import SecuritiesMgr
from strategy.find_hot_securities import FindHotSecurities

class HandleGreatIncrease(RequestBaseManager):
    
    def post (self, *args, **kwargs):

        data = json.loads(self.request.body.decode('utf-8'))

        FindHotSecurities.instance().reset()

        if "count" in data :

            FindHotSecurities.instance().limitCount = data["count"]

        if "day" in data:

            FindHotSecurities.instance().day = data["day"]

        if "endDate" in data:

            FindHotSecurities.instance().endDate = data["endDate"]

        codeInfos = None

        if data["ex"]:

            codeInfos = FindHotSecurities.instance().getHotSecuritiesEx()

        else:

            codeInfos = FindHotSecurities.instance().getHotSecurities()

        result = list()

        for codeInfo in codeInfos:

            result.append(codeInfo.toJson())

        print("finish")

        self.write({'success': 1, "data":{"codeInfos":result}})