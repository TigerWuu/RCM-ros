#!/usr/bin/env python
import numpy as np 

class RCM():
    def __init__(self,l1,l2):
        self.l1 = l1
        self.l2 = l2

    def forward(self,coord_tip,status):
		T_WA = self.transformer(self.rotation("z",status[0]),self.prismatic(0,0,0))
		T_AB = self.transformer(np.dot(self.rotation("x",-1/2*np.pi),self.rotation("z",status[1])),self.prismatic(0,0,self.l1))
		T_BC = self.transformer(self.rotation("y",-1/2*np.pi),self.prismatic(-self.l2-status[2],0,0))

		T_forward = np.eye(4)
		for i in [T_WA,T_AB,T_BC]:
			T_forward = np.dot(T_forward,i)

		coord_world = np.dot(T_forward,coord_tip)
		return coord_world

    def inverse(self):
        pass


    def transformer(self, R, P):
        T = np.concatenate((R,P),axis= 1)
        T = np.concatenate((T,np.array([[0,0,0,1]])),axis= 0)
        return T

    def rotation(self, axis, deg):
        if axis == "x":
            R = np.array([[1,          0,           0],
                          [0,np.cos(deg),-np.sin(deg)],
                          [0,np.sin(deg), np.cos(deg)]])
        elif axis == "y":
            R = np.array([[ np.cos(deg),0,np.sin(deg)],
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





