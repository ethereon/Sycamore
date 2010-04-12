#!/usr/bin/env python

'''
===========================================================

Bot Navigator
Sycamore

Copyright (C) 2010 Saumitro Dasgupta.

This code is made available under the MIT License.
<http://www.opensource.org/licenses/mit-license.html>

===========================================================

'''

from BotController import *
import xmlrpclib
from getch import *


class BotNavigator:

    bot = None
    lastBotCommand = None
    angularVelocity = 50
    linearVelocity = 200

    isBraked = False

    keyMap = {

        'w':('self.bot.driveStraight', '( self.linearVelocity, )'),
        's':('self.bot.driveStraight', '( -self.linearVelocity, )'),
        'a':('self.bot.rotate', '( self.angularVelocity, )'),
        'd':('self.bot.rotate', '( -self.angularVelocity, )'),
        'q':('self.terminate', None),
        ' ':('self.toggleState', None)

        }

    def useRemoteController(self, uri):
        
        self.bot = xmlrpclib.ServerProxy(uri, allow_none=True)
        
    def useLocalController(self, devPath):
        
        self.bot = BotController()
        self.bot.connect(devPath)
        self.bot.start()
        self.bot.enterFullMode()

    def isBotCommand(self, cmdStr):
        return ( cmdStr.find('self.bot.')==0 )

    def execCommand(self, funcName, argExp):

        cmd = eval(funcName)

        if argExp==None:
            cmd()
        else:
            args = eval(argExp)
            cmd(*args)

        if self.isBotCommand(funcName):
            self.isBraked = False
            self.lastBotCommand = (funcName, argExp)


    def terminate(self):
        
        self.isRunning = False

    def toggleState(self):

        if(self.lastBotCommand == None):
            return

        self.isBraked = not self.isBraked

        if (self.isBraked):
            self.bot.brake()
        else:
            self.execCommand(*(self.lastBotCommand))



    def navigate(self):

        self.isRunning = True

        while(self.isRunning):

            ch = getch()

            try:
                cmdTuple = self.keyMap[ch]
                self.execCommand(*cmdTuple)

            except KeyError:
                pass


        self.bot.brake()


def displayIntro():

    print "Bot Navigator for the iRobot Create\n\n"
    print " [w, s]    : Move forward / backward"
    print " [a, d]    : Rotate left / right"
    print " [space]   : Pause / Resume"
    print " q         : Terminate"
    print "\n\n"


def main():
        

    botNav = BotNavigator()

    botNav.useLocalController('/dev/ttyS0')
	
	#Uncomment the line below and comment the line above to connect
	#to a remote XML-RPC Bot Server
    #botNav.useRemoteController('http://192.168.1.3:1337')
    
    displayIntro()

    botNav.navigate()


if __name__ == "__main__":

    main()

    
