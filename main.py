import tornado.escape
import tornado.ioloop
import tornado.web

from storemgr.storemgr import SecuritiesMgr
from webserver.handleBlockInfo import HandleBlockInfo
from webserver.handleCapitalInfo import HandleCapitalInfo
from webserver.handleContinueIncrease import HandleContinueIncrease
from webserver.handleTouchHigh import HandleTouchHigh
from webserver.handleGreatIncrease import HandleGreatIncrease
from webserver.handleInIncreaseEx import HandleInIncreaseEx
from webserver.handleInIncrease import HandleInIncrease
from webserver.HandleTotalSecurities import HandleTotalSecurities

def make_app():

    return tornado.web.Application([
        ("/upload/block", HandleBlockInfo),
        ("/upload/capital", HandleCapitalInfo),
        ("/ask/continue", HandleContinueIncrease),
        ("/ask/touchHigh", HandleTouchHigh),
        ("/ask/greatIncrease", HandleGreatIncrease),
        ("/ask/checkgreatIncrease", HandleInIncreaseEx),
        ("/ask/increase", HandleInIncrease),
        ("/ask/totalsecurities", HandleTotalSecurities),
    ])

print('start load')
SecuritiesMgr.instance()
print('load finish')

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()