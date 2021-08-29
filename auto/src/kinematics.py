#!/usr/bin/env python
import numpy as np 

class kinematics():
    def __init__(self):
        pass

    def forward(self,T_list,coord_tip):
        T_forward = np.eye(3)
        for i in T_list:
            T_forward = np.dot(T_forward,i)

        coord_world = np.dot(T_forward,coord_tip)
        return coord_world

    def inverse(self):
        pass


    def tranformer(self, R, P):
        T = np.concatenate((R,P),axis= 1)
        T = np.concatenate((T,np.array([0,0,0,1])),axis= 0)
        return T

    def rotation(self, axis, deg):
        if axis == "x":
            R = np.array([[1,          0,           0],
                          [0,np.cos(deg),-np.sin(deg)],
                          [0,np.sin(deg), np.cos(deg)]])
        elif axis == "y":
            R = np.array([[ np.cos(deg),0,np,sin(deg)],
                          [ 0          ,1,          0],
                          [-np.sin(deg),0,np.cos(deg)]])
        elif axis == "z":
            R = np.array([[np.cos(deg),-np.sin(deg),0],
                          [np.sin(deg), np.cos(deg),0],
                          [0          , 0          ,1]])
        return R

    def prismatic(self, x, y, z):
        p = np.array([[x],[y],[z]])
        return p





