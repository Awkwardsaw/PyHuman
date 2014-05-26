from ctypes import *
from math import hypot
from random import uniform, randint
from time import sleep
import win32api, win32con


user = windll.user32

class Point(): 
    def __init__(self):
        pt = POINT()
        user.GetCursorPos(byref(pt))
        self.x = pt.x
        self.y = pt.y
    
    def setPoint(self, x, y):
        self.x = x
        self.y = y

class HandleMouse(object):
    
    # really kind of useless, but might be helpful
    Move_Mouse = win32con.MOUSEEVENTF_MOVE 
    Left_Down = win32con.MOUSEEVENTF_LEFTDOWN 
    Left_Up = win32con.MOUSEEVENTF_LEFTUP
    Right_Down = win32con.MOUSEEVENTF_RIGHTDOWN
    Right_Up = win32con.MOUSEEVENTF_RIGHTUP
    
    #these are for normal use
    Mouse_Left = 2 
    Mouse__Right = 8
    
    
#    def GetMousePos(self):
#        pt = POINT()       
#        user.GetCursorPos(byref(pt))
#       
#        print "GetMousePos: x = %d, y = %d" %(pt.x, pt.y)
#        return pt
        #x, y = user.GetCursorPos()
        #return x, y
        
        
    def Point_On_Bezier(self, ptl, t):
        curve = 0.03
        
        cx = curve * (ptl[1].x - ptl[0].x)
        bx = curve * (ptl[2].x - ptl[1].x) - cx
        ax = ptl[3].x - ptl[0].x - cx - bx
        
        cy = curve * (ptl[1].y - ptl[0].y)
        by = curve * (ptl[2].y - ptl[1].y) - cy
        ay = ptl[3].y - ptl[0].y - cy - by
        
        tSquared = t * t
        tCubed = tSquared * t
        
        result = Point()
        result.x = round((ax * tCubed) + (bx * tSquared) + (cx * t) + ptl[0].x)
        result.y = round((ay * tCubed) + (by * tSquared) + (cy * t) + ptl[0].y)
        
        return result
        
    def Spline(self, ex, ey, wind, CTRLP1, CTRLP2):
        pt = Point() #self.GetMousePos()  
        ep = Point()
        ep.setPoint(ex, ey)
        dist = hypot(abs(pt.x - ex), abs(pt.y - ey))
        
        ctrlPoints = [Point()  for i in range(5)]
        ctrlPoints[0] = pt
        ctrlPoints[1] = CTRLP1
        ctrlPoints[2] = CTRLP2
        ctrlPoints[3] = ep
        
        theta_inc = 1 / dist
        theta = 0.0
        
        result = [pt]
        while True:
            theta_inc += wind
            theta_inc = min(1.0 - theta, theta_inc)
            
            theta += theta_inc
            
            result.append(self.Point_On_Bezier(ctrlPoints, theta))
            if theta >= 1.0:
                break
        try:
            result[-1] = ep
        except:
            print "Error, there is no path generated"
        return result
    
    
    
    def MoveMouse(self, x, y): #instantly moves cursor to point
        pt = Point() # self.GetMousePos() 
        if pt.x != x and pt.y != y:
          user.SetCursorPos(int(x), int(y))
          
    def Move(self, x, y, rx = 0, ry = 0): #moves the cursor along a generated bezier curve
        ex = x + randint(0, rx)
        ey = y + randint(0, ry)
        CTRLP1 = Point()
        CTRLP2 = Point()
        CTRLP1.setPoint(4, 50)
        CTRLP2.setPoint(80, 37)
        
        ptl = self.Spline(ex, ey, 0.00019, CTRLP1, CTRLP2)
        for i in range(0, len(ptl)):
            self.MoveMouse(ptl[i].x, ptl[i].y)
            time.sleep(uniform(.004, .008))

    def Click(self, x, y, rx = 0, ry = 0, button = Mouse_Left):
            self.MMouse(x, y)
            win32api.mouse_event(button, 0, 0)
            time.sleep(0.05)
            win32api.mouse_event(button * 2, 0, 0)