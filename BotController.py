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

import serial
import struct
from OpenInterface import *
import time

class BotController:


	def __init__(self):
		
		#The default baudrate for the iRobot Create
		self.baudRate = 57600
		
		self.isConnected = False
		
		#If enabled, there is a forced pause after each command.
		#The reason this is often required is that a rapid succession 
		#of commands are likely to be "discarded" by the Create.
		
		self.pauseAfterCommand = True
		
		self.pauseDuration = 0.05

	def connect(self, devPath):
	    self.dev = serial.Serial(devPath, self.baudRate)
	    self.isConnected = self.dev.isOpen()

	def sendCommand(self, opcode, data=None):

	    assert self.isConnected
	    packet = opcode

	    if data!=None:
		    packet += data
        
	    self.dev.write(packet)

	    if self.pauseAfterCommand:
		    time.sleep(self.pauseDuration)

	def start(self):
	    self.sendCommand(OPCODE_START)

	def enterPassiveMode(self):
	    self.sendCommand(OPCODE_PASSIVE_MODE)

	def enterFullMode(self):
	    self.sendCommand(OPCODE_FULL_MODE)

	def enterSafeMode(self):
	    self.sendCommand(OPCODE_SAFE_MODE)

	def setMode(self, mode):

	    if mode not in BOT_MODES:
		    raise ValueError('Invalid mode specified')

	    self.sendCommand(mode)

	def drive(self, velocity, radius):

	    if (velocity<BOUND_VELOCITY_LOWER) or (velocity>BOUND_VELOCITY_UPPER):
		    raise ValueError('Velocity must be between %d to %d mm/s'%(BOUND_VELOCITY_LOWER, BOUND_VELOCITY_UPPER))

	    if ((radius<BOUND_RADIUS_LOWER) or (radius>BOUND_RADIUS_UPPER)) and (radius!=RADIUS_DRIVE_STRAIGHT):
		    raise ValueError('Radius must be between %d to %d mm'%(BOUND_RADIUS_LOWER, BOUND_RADIUS_UPPER))

    
	    kinematicDesc = struct.pack('>hh',velocity, radius)
    
	    self.sendCommand(OPCODE_DRIVE, kinematicDesc)

	def rotate(self, velocity):
	    self.drive(velocity, RADIUS_ROTATE_COUNTER_CLOCKWISE)

	def driveStraight(self, velocity):
	    self.drive(velocity, RADIUS_DRIVE_STRAIGHT);


	def brake(self):
	    self.sendCommand(OPCODE_DRIVE_DIRECT, '\x00\x00\x00\x00')
