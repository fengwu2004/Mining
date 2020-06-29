from data.securities import Securities
from data.codeInfo import CodeInfo
from data.block import BlockInfo
from storemgr.storemgr import SecuritiesMgr
from typing import Dict, List
from storemgr.excel_mananger import ExcelMgr
import datetime

_instance = None
class FindHotBlock(object):

    @classmethod
    def instance(cls):

        global _instance

        if _instance is None:

            _instance = FindHotBlock()

        return _instance

    def __init__(self):

        super().__init__()

        self.limitCount = 10

        self.year = 1

        self.endTime = 20200609

    def refreshHotBlocks(self):

        result:Dict[str, List[CodeInfo]] = dict()
    
        blockList = SecuritiesMgr.instance().blockList

        for block in blockList:

            for codeInfo in block.codeList:

                securities = SecuritiesMgr.instance().getSecurities(codeInfo)

                if securities is None:

                    continue

                today = 20191230

                error = False

                for i in range(0, self.year):

                    temp = int(today/10000) - i - 1

                    start = temp * 10000 + today % 10000

                    end = (temp + 1) * 10000 + today % 10000

                    count = securities.getCountOfLimitUp(start, end)

                    if count < self.limitCount:

                        error = True

                        break; 

                if error is True:

                    continue;

                if result.get(block.name) is None:

                    result[block.name] = []
                
                result[block.name].append(codeInfo)
                
        self.storeToExcel(result)

    def refreshHistoryIncrease(self):
    
        result:Dict[str, List[CodeInfo]] = dict()
    
        blockList = SecuritiesMgr.instance().blockList

        for block in blockList:

            for codeInfo in block.codeList:

                securities = SecuritiesMgr.instance().getSecurities(codeInfo)

                if securities is None:

                    continue

                today = self.endTime

                error = False

                for i in range(0, self.year):

                    temp = int(today/10000) - i - 1

                    start = temp * 10000 + today % 10000

                    end = (temp + 1) * 10000 + today % 10000

                    count = securities.getCountOfLimitUp(start, end)

                    if count < self.limitCount:

                        error = True

                        break

                if error is True:

                    continue

                if result.get(block.name) is None:

                    result[block.name] = []
                
                result[block.name].append(codeInfo)
                
        self.storeToExcel(result)

    def refreshHotBlocks(self):
    
        result:Dict[str, List[CodeInfo]] = dict()
    
        blockList = SecuritiesMgr.instance().blockList

        for block in blockList:

            for codeInfo in block.codeList:

                securities = SecuritiesMgr.instance().getSecurities(codeInfo)

                if securities is None:

                    continue

                today = 20191230

                error = False

                for i in range(0, self.year):

                    temp = int(today/10000) - i - 1

                    start = temp * 10000 + today % 10000

                    end = (temp + 1) * 10000 + today % 10000

                    count = securities.getCountOfLimitUp(start, end)

                    if count < self.limitCount:

                        error = True

                        break; 

                if error is True:

                    continue;

                if result.get(block.name) is None:

                    result[block.name] = []
                
                result[block.name].append(codeInfo)
                
        self.storeToExcel(result)

    def storeToExcel(self, dic:Dict[str, List[CodeInfo]]): 

        excelMgr = ExcelMgr()

        for key in dic:
            
            values = [codeInfo.name for codeInfo in dic[key]]

            excelMgr.saveRow(title = key, values = values)

        name = "/Users/aliasyan/OneDrive/mining/hot_block/hot_block_{0}_{1}_{2}.xlsx".format(self.endTime, self.limitCount, self.year)

        excelMgr.save(name)

# FindHotBlock.instance().refreshHistoryIncrease()
#
# print(FindHotBlock.instance().limitCount, "finish")

# result:Dict[str, List[CodeInfo]] = dict()

# codeInfo = CodeInfo()

# if result.get("sdk") == None:

#     result["sdk"] = []

# result["sdk"].append(codeInfo)

# print(result)

# items:List[int] = list()

# print(len(items))

# name = "hot_block_{0}.xlsx".format(100)

# print(name)

# codeInfo = CodeInfo()

# codeInfo.code = "300063"

# codeInfo.name = "天龙集团"

# sec = SecuritiesMgr.instance().getSecurities(codeInfo)

# sec.doSomeTest(20190415)
