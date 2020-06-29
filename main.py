import tornado.escape
import tornado.ioloop
import tornado.web
import datetime

from storemgr.storemgr import SecuritiesMgr
from webserver.handleBlockInfo import HandleBlockInfo
from webserver.handleCapitalInfo import HandleCapitalInfo
from webserver.handleContinueIncrease import HandleContinueIncrease
from webserver.handleTouchHigh import HandleTouchHigh
from webserver.handleGreatIncrease import HandleGreatIncrease
from webserver.handleThreeDayGreatIncreaseEx import HandleThreeDayGreatIncrease
from webserver.handleInIncrease import HandleInIncrease
from webserver.handleInDecrease import HandleInDecrease
from webserver.handleInLow import HandleInLow
from webserver.HandleTotalSecurities import HandleTotalSecurities

def make_app():

    return tornado.web.Application([
        ("/upload/block", HandleBlockInfo),
        ("/upload/capital", HandleCapitalInfo),
        ("/ask/continue", HandleContinueIncrease),
        ("/ask/touchHigh", HandleTouchHigh),
        ("/ask/greatIncrease", HandleGreatIncrease),
        ("/ask/threedaygreateincrease", HandleThreeDayGreatIncrease),
        ("/ask/increase", HandleInIncrease),
        ("/ask/decrease", HandleInDecrease),
        ("/ask/inLow", HandleInLow),
        ("/ask/totalsecurities", HandleTotalSecurities),
    ])

print('start load time = ', datetime.datetime.now())
SecuritiesMgr.instance()
print('load finish time = ', datetime.datetime.now())

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()