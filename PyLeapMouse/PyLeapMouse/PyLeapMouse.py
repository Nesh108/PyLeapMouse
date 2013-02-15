################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys
import ctypes
import win32api, win32con
from time import sleep

class LeapListener(Leap.Listener):    
    
    DEBUG = False
    fingers_count = 0
    prev_fingers_count = 0
    SLOW = 0.010;
    
    #Screen resolution, it should match the current screen resolution for more precise movements
    SCREEN_X = 0
    SCREEN_Y = 0

    cur_x = 0
    cur_y = 0
    
    Lclicked = False
    Rclicked = False
    keystroke = False
    LHold = False

    def on_init(self, controller):
        user32 = ctypes.windll.user32
        self.SCREEN_X = user32.GetSystemMetrics(0)
        self.SCREEN_Y = user32.GetSystemMetrics(1)
        print "Current screen resolution: {0} x {1}".format(self.SCREEN_X, self.SCREEN_Y)
        
        print "Initialized"


    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        
        # Get the most recent frame and report some basic information
        frame = controller.frame()
                                       
        if not frame.fingers.empty:
            # Get Fingers
            fingers = frame.fingers
            self.fingers_count = fingers.__len__();
            
            if LeapListener.DEBUG and self.fingers_count != self.prev_fingers_count:
                print "Currently %s fingers visible.\n" % self.fingers_count
                self.prev_fingers_count = self.fingers_count
                
            
            if not fingers.empty:
                # Calculate the hand's average finger tip position
                avg_pos = Leap.Vector()
                for finger in fingers:
                    avg_pos += finger.tip_position
                avg_pos /= len(fingers)
            
            
            moveMouse(self, int(avg_pos.x*15), int(self.SCREEN_X - avg_pos.y*5))
            
            
            
            
    
            
def slow(self):
    sleep(self.SLOW)           
            
def moveMouse(self, x, y):    
    if self.cur_x != x or self.cur_y != y:      
        self.cur_x = x
        self.cur_y = y
        win32api.SetCursorPos((int(x),int(y)))  

# 0: Left
# 1: Right
# 2: Middle  -not implemented yet-        
def clickMouse(value):
    global cur_x, cur_y    
    
    if value == 0:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,cur_x, cur_y,0,0)
    else:
        if value == 1:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,cur_x, cur_y,0,0)
        else:
            if value == 2:
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN,cur_x, cur_y,0,0)
    
# 0: Left
# 1: Right
# 2: Middle  -not implemented yet-        
def releaseMouse(value):
    global cur_x, cur_y    
    
    if value == 0:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,cur_x, cur_y,0,0)
    else:
        if value == 1:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,cur_x, cur_y,0,0)
        else:
            if value == 2:
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP,cur_x, cur_y,0,0)          


def main():
    # Create a sample listener and controller
    listener = LeapListener()
    controller = Leap.Controller()

    if raw_input('Do you want to enable Debug Mode? Y/N (Default: Disabled)') == 'Y':
        LeapListener.DEBUG = True
        print "Debug Mode Enabled."
    else:
        print "Default: Debug Mode Disabled."
    

    
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
