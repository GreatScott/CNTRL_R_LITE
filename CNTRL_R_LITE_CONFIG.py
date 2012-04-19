# CNTRL:R Lite Script
# A SUPER-stripped down version of Aumhaa's (http://aumhaa.blogspot.com) CNTRL:R script. 
#
# Written by Scott Novich (Great Scott) - http://soundcloud.com/greatscott
#
# Contact: scott@glitch.fm
#
# Gr33tz to my homie willmarshall (http://willmarshall.me/)
#
# This file is designed to abstract away all of messy coding to customize your controller.
#
# First, you will need to reference your CNTRL:R's hard-coded MIDI assignments (internal to the controller itself).
# By default (if you haven't messed around with the CNTRL:R editor and sent the changes) you can find them here:
# http://wiki.lividinstruments.com/wiki/File:CNTRLR_MIDI_Defaults.png
# By default, all buttons (the 4x4, 16x2, and push-buttons on the center encoders are of type "Note." All encoders/faders themselves are of type "CC."
#
# If you change these in the CNTRL:R editor, you will need to refer to those instead...
#
# Color/flashing light conventions:
# 7 colors available: C_OFF (LED off), C_YELLOW, C_CYAN, C_VIOLET, C_RED, C_GREEN, C_WHITE
# 3 blinking speeds available (you can modify CNTRL_R_LITE_DEFS.py to add more/tweak these): S_FAST, S_MED, S_SLOW
# To make a color blink, just add to it it's speed variable.
#
# Assignment examples:
# SOMEBUTTON = C_CYAN (the button will be statically lit cyan)
# SOMEBUTTON = C_YELLOW+S_MED (the button will blink yellow at a medium rate)
#
# You can add other speeds/tweak the defined speeds in CNTRL_R_LITE_DEFS.py
# 

from CNTRL_R_LITE_DEFS import * # This line imports a set of simple definitions CNTRL_R_LITE_DEFS.py to make this file easier to read + customize.

# PART 1: Setting up your session view (the red box / clip grid) if you want it. 
# Default in this script is to use CNTRL:R's 4x4 grid, but you could *easily* modify this to use the 16x2 grid, or any other combo.
USE_SESSION_VIEW = True # Set to false if you don't want this feature

N_TRACKS = 4 # How many tracks wide the red box should be. 4 is suggested if you want to use your CNTRL:R's 4x4 Grid
N_SCENES = 4 # How many scenes deep the red box should be. 4 is suggested if you want to use your CNTRL:R's 4x4 Grid

# Refer to http://wiki.lividinstruments.com/wiki/File:CNTRLR_MIDI_Defaults.png.

# TRACK_CLIP_BUTTONS layout is laid out as [TRACK1 buttons | TRACK2 buttons | etc]
# EXAMPLE: TRACK_CLIP_BUTTONS = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
# If N_TRACKS = 4, and N_SCENES = 4, this will assign Track1's Clip Cells to 0,1,2,3 ; Track2's to 4,5,6,7 ; etc
TRACK_CLIP_BUTTONS = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] # Must be N_TRACKS x N_SCENES in length

# Available colors: C_OFF, C_YELLOW, C_CYAN, C_VIOLET, C_RED, C_GREEN, C_WHITE. Available speeds: S_FAST, S_MED, S_SLOW
CLIP_STARTED_COLOR = C_GREEN # clip currently playing color
CLIP_STOP_COLOR = C_WHITE # clip not currently playing color, but there is one in the cell
CLIP_TRG_PLAY_COLOR = C_GREEN+S_FAST # clip triggered but not yet playing color (used if clip trigger is quantized to grid)

USE_SESSION_NAV = True # This will tie additional buttons to your control for moving the red-box/clip-grid around in Live
NAVBOX_LEFT_BUTTON = 22
NAVBOX_LEFT_BUTTON_C = C_YELLOW
NAVBOX_RIGHT_BUTTON = 23
NAVBOX_RIGHT_BUTTON_C = C_YELLOW
NAVBOX_UP_BUTTON = 24
NAVBOX_UP_BUTTON_C = C_YELLOW
NAVBOX_DOWN_BUTTON = 40
NAVBOX_DOWN_BUTTON_C = C_YELLOW

# PART 2: Setting up your basic mixer controls. The mixer is comprised of channel strips (like on a real mixer) in live. 
# This will allow you to give mixer control over your session view. Specifically: Volume, Mute, Solo, Sends.
# Each track on the mixer will correspond to a track in our session view. This means, if you assign a button to Mute on the first track in this mixer,
# it will control the first ** SESSION VIEW TRACK** (not the global track number) in Ableton Live. So if you move the red box around, the button assignment will update accordingly.
USE_MIXER_CONTROLS = True
# NOTE: If turned on, this will create a mixer that is the same size as N_TRACKS. If you do something like create a 16x2 clip nav grid in Part 1 - it's OK - you're not obligated to
# assign knobs/faders for everything.

N_SENDS = 2
USE_MIXER_EQ = False
USE_MIXER_FILTERS = False

USE_MUTE_BUTTONS = False
MUTE_BUTTONS = [16,19,26,29] # Refer to http://wiki.lividinstruments.com/wiki/File:CNTRLR_MIDI_Defaults.png.
MUTE_BUTTON_COLOR = C_YELLOW

USE_SOLO_BUTTONS = False
SOLO_BUTTONS = [32,35,42,45]
SOLO_BUTTON_COLOR = C_CYAN


# PART 3: Device Assignments (TO DO)

