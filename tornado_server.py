#!/usr/bin/env python

from tornado.options import options, define, parse_command_line
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import tornado.websocket
import json
import time
from random import randint
from main import *

define('port', type=int, default=5500)

class HelloHandler(tornado.web.RequestHandler):
  def get(self):
    self.write('Hello from tornado')

class MyWebSocket(tornado.websocket.WebSocketHandler):
  clients = []

  def check_origin(self, origin):
      return True

  def open(self):
    # clients must be accessed through class object!!!
    res = '{"response":"opened"}'
    self.write_message(res)
    MyWebSocket.clients.append(self)
    print "\nWebSocket opened"

  def on_message(self, message):
    print "msg recevied", message

    msg = json.loads(message)

    if (msg["request"] == "connect"):
        res = '{"response":"connected"}'
        self.write_message(res)

    # if (msg["request"] == "start"):
    #     res = '{"response":"streaming"}'
    #     self.write_message(res)
    #     for x in range(0, 20):
    #         randomNum = randint(1,100)
    #         print "We're on time %d" % (randomNum)
    #         value = '{"result":' + str(randomNum) + '}'
    #         self.write_message(json.loads(value))
    #         time.sleep(1)

    if (msg["request"] == "start"):

        res = getResults()

        if (res == False):
            value = '{"response":' + 'error' + '}'
            self.write_message(json.loads(value))
        else:
            print(type(res))
            value = '{"response":"success","result":' + res + '}'
            self.write_message(json.loads(value))

  def on_close(self):
    print "WebSocket closed"
    # clients must be accessed through class object!!!
    res = '{"response":"closed"}'
    self.write_message(res)
    MyWebSocket.clients.remove(self)

def main():
  tornado_app = tornado.web.Application([
      ('/hello-tornado', HelloHandler),
      ('/websocket', MyWebSocket),
      ])
  server = tornado.httpserver.HTTPServer(tornado_app)
  server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
  main()
