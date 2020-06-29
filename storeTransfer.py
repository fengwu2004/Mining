from data.securities import Securities
from data.codeInfo import CodeInfo
from data.block import BlockInfo
from data.klineModel import KLineModel
from storemgr.storemgr import SecuritiesMgr
from typing import Dict, List
from datetime import datetime

import psycopg2
import json

conn = psycopg2.connect("hostaddr=127.0.0.1 port=5432 user=postgres dbname=stock")

cur = conn.cursor()

cur.execute("CREATE TABLE if not exists securities (id serial PRIMARY key, code varchar, name varchar, capital real)")

cur.execute("delete from securities")

def kLineValues(kLines:[KLineModel]):

    values = ""

    value = ""

    for kLine in kLines:

        if len(value) > 0:

            values += value

            values += ","

        value = "(%d, %f, %f, %f, %f, %f)" % (kLine.date, kLine.high, kLine.low, kLine.open, kLine.close, kLine.preClose)

    if len(value) > 0:

        values += value

        values += ";"

    return values

def securitiesValue(securitiesInfo:Securities):

    value = "('%s', '%s', %f)" % (securitiesInfo.codeInfo.code, securitiesInfo.codeInfo.name, securitiesInfo.capital)

    return value

for securities in SecuritiesMgr.instance().securitiesList:

    if securities.isST() or securities.isSTIB():

        continue

    sql = "insert into securities (code, name, capital) values %s" % securitiesValue(securities)

    cur.execute(sql)

    cur.execute("CREATE TABLE if not exists kline_day_%s (id serial PRIMARY key, date integer, high real, low real, open real, close real, preClose real)" % securities.codeInfo.code)

    cur.execute("delete from kline_day_%s" % securities.codeInfo.code)

    kLinevalues = kLineValues(securities.klines)

    if len(kLinevalues) > 0:

        sql = "insert into kline_day_%s (date, high, low, open, close, preClose) values %s" % (securities.codeInfo.code, kLinevalues)

        cur.execute(sql)

conn.commit()

print("ok", datetime.now())