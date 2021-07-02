import os
import time
if os.name=="nt": os.system('cls')
else: os.system('clear')
import sys
import cv2 as cv
import numpy as np
import random as rnd
from math import radians, sin,cos,sqrt,atan2,exp
from time import time as TIME
from time import ctime
import signal # used in main
import pickle # used in main
import matplotlib.pyplot as plt
from psutil import disk_usage
from termcolor import colored 
from itertools import combinations  as comb , product
from datetime import datetime

def m2px(inp):
    return int(inp*512/2)

def DirLocManage(returnchar=False):
    ''' with this segment code is callable from any folder '''
    if os.name=='nt':
        dirChangeCharacter='\\'
    else:
        dirChangeCharacter='/'
    if returnchar==False:
        scriptLoc=__file__
        for i in range(len(scriptLoc)):
            # if '/' in scriptLoc[-i-2:-i]: # in running
            if dirChangeCharacter in scriptLoc[-i-2:-i]: # in debuging
                scriptLoc=scriptLoc[0:-i-2]
                break
        # print('[+] code path',scriptLoc)
        os.chdir(scriptLoc)
    return dirChangeCharacter
    ''' done '''

def construct_arena(Lx,Ly,Qtable,actionSpace,QRpos_ar,visibleRaduis):
    arena=np.zeros((Ly,Lx,3))+255
    """ QR locations """
    for i in QRpos_ar:
        cv.circle(arena,tuple(i),10,0,-1)
        cv.circle(arena,tuple(i),visibleRaduis,0,1)
    """ cue location """
    cv.circle(arena,(Lx//2,3*Ly//4),m2px(0.7),(0,0,0),2)

    Qtable=Qtable[1:] #! removing first row of Qtable because of Q0
    states=np.arange(0,Qtable.shape[0]) #! for debugging
    # states=np.arange(5,6)
    for state in states:
        p1=QRpos_ar[state]
        angle_correction= 180 if state<3 else 0
        for counter,action in enumerate(actionSpace):
            cartesian_action=np.array([action[0]*np.sin(np.radians(angle_correction+action[1])) \
                , action[0]*np.cos(np.radians(angle_correction+action[1]))])
            p2=p1+cartesian_action
            reward=int(min((Qtable[state][counter]+1)*(255/101),255))
            reward=255-reward
            cv.circle(arena,(int(p2[0]),int(p2[1])),5,(reward,reward,reward),-1)
            # cv.circle(arena,(int(p2[0]),int(p2[1])),5,0,-1)
    return arena

if __name__ == "__main__":
    DirLocManage()
    # Qtable=np.genfromtxt('49010.csv', delimiter=',')
    Qtable=np.genfromtxt('99010.csv', delimiter=',')
    """ max reward 100 min reward -1 """
    Lx=Xlen=m2px(2)
    Ly=Ylen=m2px(4)
    # angles=np.array([45,90,90+45])
    angles=np.arange(0,180+18,18)
    maxlen=int(np.sqrt(Xlen**2+Ylen**2))
    lens=[4*maxlen//4,3*maxlen//4,2*maxlen//4,1*maxlen//4]
    actionSpace=list(product(lens,angles))
    QRloc={'QR1':( Lx, Ly//4),'QR2':( Lx, Ly//4*2),'QR3':( Lx, Ly//4*3),'QR4':(0,3* Ly//4),'QR5':(0,2* Ly//4),'QR6':(0, Ly//4)}
    QRpos_ar=np.array(list(QRloc.values()))
    visibleRaduis=m2px(0.3)
    arena=construct_arena(Lx,Ly,Qtable,actionSpace,QRpos_ar,visibleRaduis)
    cv.imwrite("arena.png",arena) #! imshow gets colors between 0 and 1
    cv.imshow("arena",arena/255) #! imshow gets colors between 0 and 1
    cv.waitKey()
print("HI")