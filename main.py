import tornado.escape
import tornado.ioloop
import tornado.web

from storemgr.storemgr import SecuritiesMgr
from webserver.handleBlockInfo import HandleBlockInfo
from webserver.handleContinueIncrease import HandleContinueIncrease

def make_app():

    return tornado.web.Application([
        ("/upload/block", HandleBlockInfo),
        ("/ask/continue", HandleContinueIncrease),
    ])

print('start load')
SecuritiesMgr.instance()
print('load finish')

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()