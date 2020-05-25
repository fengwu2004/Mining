import numpy
import pandas
from data.securities import Securities
from storemgr.storemgr import SecuritiesMgr
from data.codeInfo import CodeInfo
from data.klineModel import KLineModel
import matplotlib.pyplot as plt

cdkj = SecuritiesMgr.instance().getSecurities(codeInfo = CodeInfo(code = "600584", name = "长电科技"))

jfkj = SecuritiesMgr.instance().getSecurities(codeInfo = CodeInfo(code = "600519", name = "贵州茅台"))

print(cdkj)

cdkjClose = [x.close for x in cdkj.klines]

jfkjClose = [x.close for x in jfkj.klines]

df1 = pandas.DataFrame(numpy.array(cdkjClose), columns=[cdkj.codeInfo.name])

df2 = pandas.DataFrame(numpy.array(jfkjClose), columns=[jfkj.codeInfo.name])

df = pandas.concat([df1, df2], axis = 1)

corr = df.corr(method="pearson", min_periods=1)

df1.to_csv("cdkj_jfkj.csv")

df.plot(figsize=(20,12))

plt.savefig("cdkj.png")

plt.close()

print(corr)
