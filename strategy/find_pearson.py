import numpy
import pandas
from data.securities import Securities
from storemgr.storemgr import SecuritiesMgr
from data.codeInfo import CodeInfo
from data.klineModel import KLineModel
import matplotlib.pyplot as plt


def testFun():

    allSecurities = SecuritiesMgr.instance().securitiesList

    result = []

    for securities in allSecurities:

        close = [x.close for x in securities.klines]

        dates = [x.date for x in securities.klines]

        data = numpy.array([dates, close])

        data = numpy.transpose(data)

        df = pandas.DataFrame(data=data[0:,1:], index=data[0:,0], columns=[securities.codeInfo.name])

        result.append(df)

    df = pandas.concat(result, axis=1)

    corr = df.corr(method="pearson", min_periods=1)

    corr.to_excel("total.xlsx")

testFun()