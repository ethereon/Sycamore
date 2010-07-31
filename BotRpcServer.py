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

import socket
import xmlrpclib
import sys
from optparse import OptionParser
from SimpleXMLRPCServer import SimpleXMLRPCServer
from BotController import BotController
from SimController import SimController
from threading import Timer

class CommandDispatch:

    

    def __init__(self, botController, cutoff):

        self.bot = botController
        self.cutoff = cutoff
        self.timer = None

    def msg(self, msg):

        print '[ Command Dispatch ] ', msg

    def cutoffPassed(self):
        self.msg("Cut off passed. Stopping robot...")
        self.bot.brake()

    def _dispatch(self, method, params):

        try:
            func = getattr(self.bot,method)
        except AttributeError:
            raise Exception('Method "%s" is not supported.' % method)

        else:

            #Reset the timer
            if self.timer!=None : self.timer.cancel()

            self.timer = Timer(self.cutoff, self.cutoffPassed)

            self.timer.start()

            # Note that there is a potential security issue here!
            # There are no checks to limit the methods called.
            return apply(func, params)



class BotServer:

    def __init__(self, commandDispatch):
        
        self.commandDispatch = commandDispatch


    def start(self, listenAddress, listenPort):

        self.server = SimpleXMLRPCServer((listenAddress, listenPort), allow_none=True)
        self.server.register_instance(self.commandDispatch)
        print "XML RPC BotServer started on %s:%d"%(str(listenAddress), listenPort)
        self.server.serve_forever()
        



def main():

    DEFAULT_PORT = 1337

    #Parse command line arguments

    parser = OptionParser(usage='%prog [options] device_path (eg : /dev/ttyS0)',
                          description = 'Sycamore RPC Server for iRobot Create')

    parser.add_option('-s','--simulate', action='store_true', dest='simulate', help = 'Use simulated bot controller')
    parser.add_option('-c','--cutoff', dest='cutoff', type='float', help = 'Cutoff time ( real number, seconds )')
    parser.add_option('-p','--port', dest='port', type='int', help = 'Listening port ( default = %d )'%DEFAULT_PORT)


    (options, args) = parser.parse_args()

    if len(args)!=1:
        parser.error('Incorrect number of arguments')


    #Configure the bot controller

    if options.simulate:
        botController = SimController()
    else:
        botController = BotController()


    botController.connect(args[0])
    botController.start()
    botController.enterFullMode()

    #Configure the server

    if options.cutoff:
        dispatch = CommandDispatch(botController, options.cutoff)
    else:
        dispatch = botController

    servPort = options.port if options.port else DEFAULT_PORT

    servAddress = socket.gethostbyname(socket.gethostname())

    #Start the server

    botServer = BotServer(dispatch)

    botServer.start(servAddress, servPort)


if __name__ == "__main__":
    main()
