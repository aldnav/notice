
""" Simple APN Server
@author: Aldrin Navarro
@date: Dec. 2, 2015
"""

import uuid

from tornado import websocket, web, ioloop
from tornado.options import define, options

define("port", default=8888, help="run APN on the given port", type=int)

clients = {}


class SocketHandler(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print 'opening'
        self.id = uuid.uuid4()
        self.stream.set_nodelay(True)
        clients[self.id] = {'id': self.id, 'object': self}
        print clients

    def on_message(self, message):
        print "Client %s received a message : %s" % (self.id, message)

    def on_close(self):
        print 'closing'
        if self.id in clients:
            del clients[self.id]


app = web.Application([
    (r'/', SocketHandler),
])

if __name__ == '__main__':
    app.listen(options.port)
    ioloop.IOLoop.instance().start()
