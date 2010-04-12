#!/usr/bin/env python

'''
===========================================================

Remote Bot Control via XML-RPC
Sycamore

Copyright (C) 2010 Saumitro Dasgupta.

This code is made available under the MIT License.
<http://www.opensource.org/licenses/mit-license.html>

===========================================================

'''


import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
from BotController import BotController



class BotServer:

    def __init__(self, devLocation):

        self.bot = BotController()
        self.bot.connect(devLocation)
        self.bot.start()
        self.bot.enterFullMode()

        

    def registerFunctions(self):

        self.server.register_function(self.bot.driveStraight, 'driveStraight')
        self.server.register_function(self.bot.rotate, 'rotate')
        self.server.register_function(self.bot.drive, 'drive')
        self.server.register_function(self.bot.brake, 'brake')
        

    def start(self, listenAddress, listenPort):

        self.server = SimpleXMLRPCServer((listenAddress, listenPort), allow_none=True)
        self.registerFunctions()
        print "XML RPC BotServer started on port %d"%(listenPort)
        self.server.serve_forever()
        




def main():

    botServer = BotServer('/dev/ttyS0')

    botServer.start('localhost', 1337)


if __name__ == "__main__":
    main()
