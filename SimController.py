#!/usr/bin/env python

'''
===========================================================

Simulated Robot Interface
Sycamore

Copyright (C) 2010 Saumitro Dasgupta.

This code is made available under the MIT License.
<http://www.opensource.org/licenses/mit-license.html>

===========================================================

'''

from OpenInterface import *

class SimController:


	def __init__(self):
		
		self.isConnected = False
	
	def msg(self, tag, msg):

		print '[ SimCon | %s ] %s'%(tag,msg)

	def connect(self, devPath):
	    
		self.isConnected = True
		self.msg('Core','Connection to robot at %s requested.'%(devPath))
		
	def notifyAction(self, actionMsg):
		
		assert self.isConnected

		self.msg('Robot State' , actionMsg)
		
	def start(self):
		self.notifyAction('Started.')

	def enterPassiveMode(self):
		self.notifyAction('Entered passive mode.')

	def enterFullMode(self):
		self.notifyAction('Entered full mode.')
		
	def enterSafeMode(self):
		self.notifyAction('Entered passive mode.')

	def setMode(self, mode):
	    
		if mode not in BOT_MODES:
			raise ValueError('Invalid mode specified')

		self.notifyAction('Changing mode to ' + str(mode))

	def checkVelocityBounds(self, velocity):

		if (velocity<BOUND_VELOCITY_LOWER) or (velocity>BOUND_VELOCITY_UPPER):
			raise ValueError('Velocity must be between %d to %d mm/s'%(BOUND_VELOCITY_LOWER, BOUND_VELOCITY_UPPER))

	def drive(self, velocity, radius):
	
		self.checkVelocityBounds(velocity)
		
		if ((radius<BOUND_RADIUS_LOWER) or (radius>BOUND_RADIUS_UPPER)) and (radius!=RADIUS_DRIVE_STRAIGHT):
			raise ValueError('Radius must be between %d to %d mm'%(BOUND_RADIUS_LOWER, BOUND_RADIUS_UPPER))

		self.notifyAction('Driving at %d mm/s with a radius of %d mm.'%(velocity, radius))


	def rotate(self, velocity):
	
		self.checkVelocityBounds(velocity)
		
		if velocity>0:
			polarity = 'counter-clockwise'
		else:
			polarity = 'clockwise'
			
		self.notifyAction('Rotating %s.'%(polarity))

	def driveStraight(self, velocity):
	
		self.checkVelocityBounds(velocity)
		
		self.notifyAction('Driving straight at a velocity of %d mm/s.'%(velocity))
		

	def brake(self):
	
		self.notifyAction('Stopped moving.')
		
