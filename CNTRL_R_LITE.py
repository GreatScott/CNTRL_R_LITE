# CNTRL:R Lite Script
# A SUPER-stripped down version of Aumhaa's (http://aumhaa.blogspot.com) CNTRL:R script. 
#
# ASSIGNMENTS: See CNTRL_R_LITE_CONFIG.py
#
# Written by Scott Novich (Great Scott) - http://soundcloud.com/greatscott
#
# Contact: scott@glitch.fm
#
# Gr33tz to my homie willmarshall (http://willmarshall.me/).
#
# Version 1.0 
# Latest revision date: 4/12/2012
#
# List of references worth checking out:
# 1. Intro to remote scripting: http://remotescripts.blogspot.com/2010/03/introduction-to-framework-classes.html
# 2. CNTRL:R's default MIDI assignments http://wiki.lividinstruments.com/wiki/File:CNTRLR_MIDI_Defaults.png
# 3. Framework reference doc if you want to expand on this script: http://hanzoffsystems.tech.officelive.com/_Framework_822/default.aspx
# 4. Check out Will Marshall's (http://willmarshall.me/) and Aumhaa's+Livid's (http://blog.lividinstruments.com/2011/04/20/controller-apps/) scripts for some fancier stuff like device control, session zoom (navigating around individual tracks), etc.
# 
#
# Forthcoming in later versions / To-Do:
# 1: Device assignment examples
# 2: Session zoom examples
# 3: Flashing color support examples
# 4: Session view color assignments tied to clip color in ableton (... not sure if possible yet)


import Live
import time

from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from _Framework.ButtonElement import ButtonElement # Class representing a button a the controller
from _Framework.ButtonMatrixElement import ButtonMatrixElement # Class representing a 2-dimensional set of buttons
from _Framework.ChannelStripComponent import ChannelStripComponent # Class attaching to the mixer of a given track
from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
from _Framework.InputControlElement import * # Base class for all classes representing control elements on a controller
from _Framework.SceneComponent import SceneComponent # Class representing a scene in Live
from _Framework.SessionComponent import SessionComponent # Class encompassing several scene to cover a defined section of Live's session
from _Framework.SliderElement import SliderElement # Class representing a slider on the controller
from _Framework.EncoderElement import EncoderElement # Class representing a continuous control on the controller

from FlashingButtonElement import FlashingButtonElement # Custom code from Aumhaa/livid for creating flashing buttons
from CNTRL_R_LITE_CONFIG import * # This contains your custom-tailored configuration/layout. This is really the only thing you should be editing.
from CNTRL_R_LITE_DEFS import * # This contains some abstractions for making code more readable/easy to modify


# Global Variables
CHANNEL = 0 # assume channel is constant for everything

class CNTRL_R_LITE(ControlSurface):
	def __init__(self, c_instance):
		ControlSurface.__init__(self, c_instance)
		is_momentary = True
		self._timer = 0 # Used in FlashingButtonElement (kludge for our purposes)
		self.flash_status = 1 # Used in FlashingButtonElement (kludge for our purposes)		
		
		if USE_MIXER_CONTROLS == True:
			self.mixer_control()
		
		if USE_SESSION_VIEW == True:
			self.session_control()		
  
	def mixer_control(self):
		self.num_tracks = N_TRACKS
		self.mixer = MixerComponent(N_TRACKS, N_SENDS, USE_MIXER_EQ, USE_MIXER_FILTERS)
		self.mixer.name = 'Mixer'
		self.mixer.set_track_offset(0) #Sets start point for mixer strip (offset from left)
		for index in range(N_TRACKS):
			self.mixer.channel_strip(index).name = 'Mixer_ChannelStrip_' + str(index)
			self.mixer.channel_strip(index)._invert_mute_feedback = True 
		self.song().view.selected_track = self.mixer.channel_strip(0)._track
	
		#if USE_MUTE_BUTTONS == True:
		#for index in range(len(MUTE_BUTTONS)):
	    

	  
	def session_control(self):
		is_momentary = True
		self._timer = 0
		self.flash_status = 1
		self.grid = [None for index in range(N_TRACKS*N_SCENES)]
		for index in range(N_TRACKS*N_SCENES):
			self.grid[index] = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,TRACK_CLIP_BUTTONS[index], 'Grid' + str(index), self)
		self.matrix = ButtonMatrixElement()
		for row in range(4):
			button_row = []
			for column in range(4):
				button_row.append(self.grid[row+(column*4)])
			self.matrix.add_row(tuple(button_row))
		self.session = SessionComponent(N_TRACKS,N_SCENES)
		self.session.name = "Session"
		self.session.set_offsets(0,0)
		self.scene = [None for index in range(N_SCENES)]
		for row in range(N_SCENES):
			self.scene[row] = self.session.scene(row)
			self.scene[row].name = 'Scene_'+str(row)
			for column in range(N_TRACKS):
				clip_slot = self.scene[row].clip_slot(column)
				clip_slot.name = str(column)+'_Clip_Slot'+str(row)
				self.scene[row].clip_slot(column).set_triggered_to_play_value(CLIP_TRG_PLAY_COLOR)
				self.scene[row].clip_slot(column).set_stopped_value(CLIP_STOP_COLOR)
				self.scene[row].clip_slot(column).set_started_value(CLIP_STARTED_COLOR)
	
    # Clip trigger on grid assignments
		for column in range(4):
			for row in range(4):
				self.scene[row].clip_slot(column).set_launch_button(self.grid[row+(column*4)])	
	
		for index in range(N_TRACKS*N_SCENES):
			self.grid[index].clear_send_cache()	  
				
		if USE_SESSION_NAV == True:
			self.navleft = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,NAVBOX_LEFT_BUTTON, 'Nav_Left_Button', self)
			self.navleft.clear_send_cache()
			self.navleft.set_on_off_values(NAVBOX_LEFT_BUTTON_C, NAVBOX_LEFT_BUTTON_C)
			
			self.navright = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,NAVBOX_RIGHT_BUTTON, 'Nav_Right_Button', self)
			self.navright.clear_send_cache()
			self.navright.set_on_off_values(NAVBOX_RIGHT_BUTTON_C, NAVBOX_RIGHT_BUTTON_C)
			
			self.navup = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,NAVBOX_UP_BUTTON, 'Nav_Up_Button', self)
			self.navup.clear_send_cache()
			self.navup.set_on_off_values(NAVBOX_UP_BUTTON_C, NAVBOX_UP_BUTTON_C)
				 
			self.navdown = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,NAVBOX_DOWN_BUTTON, 'Nav_Down_Button', self)
			self.navdown.clear_send_cache()
			self.navdown.set_on_off_values(NAVBOX_DOWN_BUTTON_C, NAVBOX_DOWN_BUTTON_C) 
			
			self.session.set_track_bank_buttons(self.navright, self.navleft) # L-R CTRLR 23, 22
			self.session.set_scene_bank_buttons(self.navdown, self.navup) # U-D CTRLR 40,24	  
		
		if USE_MIXER_CONTROLS == True:
			self.session.set_mixer(self.mixer)	

		self.refresh_state()
		self.session.set_enabled(True)
		self.session.update()		
			
	def update_display(self):
		ControlSurface.update_display(self)
		self._timer = (self._timer + 1) % 256
		self.flash()
		
	def flash(self):
		for index in range(N_TRACKS*N_SCENES):
			if(self.grid[index]._flash_state > 0):
				self.grid[index].flash(self._timer)	
		if(self.navleft._flash_state>0):
				self.navleft.flash(self._timer)
		if(self.navright._flash_state>0):
				self.navright.flash(self._timer)
		if(self.navup._flash_state>0):
				self.navup.flash(self._timer)
		if(self.navdown._flash_state>0):
				self.navdown.flash(self._timer)				

	def disconnect(self):
		self._hosts = []
		self.log_message("--------------= CNTRLR log closed =--------------")
		ControlSurface.disconnect(self)
		return None		