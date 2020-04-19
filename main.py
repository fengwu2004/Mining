import tornado.escape
import tornado.ioloop
import tornado.web

from webserver.handleBlockInfo import HandleBlockInfo

def make_app():

    return tornado.web.Application([
        ("/upload/block", HandleBlockInfo),
    ])

# SecuritiesMgr.instance()
# print('load finish')

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()