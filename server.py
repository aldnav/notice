
""" Simple Push Notification Server
@author: Aldrin Navarro
@date: Dec. 2, 2015
"""

import json
import logging
import requests
import uuid

from tornado import websocket, web, ioloop
from tornado.options import define, options

import settings

define("port", default=8888, help="run APN on the given port", type=int)

PROJECT_ID = settings.PROJECT_ID
clients = {}
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NotifyClientHandler(web.RequestHandler):

    @web.asynchronous
    def get(self, *args):
        _clients = self.get_arguments('client')
        context = self.get_argument('context')
        payload = json.dumps({'type': 'notification', 'value': str(context)})
        # NOTE: not working yet, need to remove idle clients from db
        for client in _clients:
            if client not in clients:
                FALLBACK_URL = settings.FALLBACK_URL
                requests.get(FALLBACK_URL, params={'client_id': client})
                continue
            ws = clients[client]['object']
            ws.write_message(payload)
        self.set_status(200)
        self.finish()


class SocketHandler(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        # TODO: Better authentication or handshake mech
        # authenticate
        if PROJECT_ID != self.get_argument('PROJECT_ID'):
            self.close(code=1011, reason='Unauthorized request.')
        # Register as client
        self.id = str(uuid.uuid4())
        self.stream.set_nodelay(True)
        clients[self.id] = {'id': self.id, 'object': self}
        # send back registration id
        payload = json.dumps({'type': 'registration', 'value': str(self.id)})
        self.write_message(payload)

    def on_message(self, message):
        pass

    def on_close(self):
        # unregister
        if self.id in clients:
            del clients[self.id]

# Application

conf = {
    'debug': True,
    'cookie_secret': PROJECT_ID
}

app = web.Application([
    (r'/ws', SocketHandler),
    (r'/', NotifyClientHandler),
], **conf)

if __name__ == '__main__':
    options.parse_command_line()
    app.listen(options.port)
    ioloop.IOLoop.instance().start()
