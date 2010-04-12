'''
===========================================================

iRobot Create Open Interface Constants
Sycamore

Copyright (C) 2010 Saumitro Dasgupta.

This code is made available under the MIT License.
<http://www.opensource.org/licenses/mit-license.html>

===========================================================

'''

OPCODE_START = '\x80'

OPCODE_DRIVE = '\x89'

OPCODE_PASSIVE_MODE = '\x80' #Start puts the create in passive mode

OPCODE_SAFE_MODE = '\x83'

OPCODE_FULL_MODE = '\x84'

OPCODE_DRIVE_DIRECT = '\x91'

BOUND_VELOCITY_LOWER = -500

BOUND_VELOCITY_UPPER = 500

BOUND_RADIUS_LOWER = -2000

BOUND_RADIUS_UPPER = 2000

RADIUS_ROTATE_COUNTER_CLOCKWISE = 0x01

RADIUS_DRIVE_STRAIGHT = 0x7FFF
