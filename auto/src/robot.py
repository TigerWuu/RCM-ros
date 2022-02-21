#!/usr/bin/env python3

""" 
-------------------------
Author : Jing-Shiang Wuu
Date : 2021/9/7
Institution : National Taiwan University 
Department : Bio-Mechatronics Engineering
Status : Senior
-------------------------
Description:
"""


import numpy as np 

class RCM():
	def __init__(self,l1,l2):
		self.l1 = l1
		self.l2 = l2

	def forward(self,coord_tip,status):
		theta1 = status[0]
		theta2 = status[1] ## be cautios of the up and down angle
		d = status[2]*1000.0 # m to mm

		R1 = self.rotation("z",theta1)
		P1 = self.prismatic(0,0,0)
		# eular angle
		# R2 = np.dot(self.rotation("x",-np.pi/2),self.rotation("z",theta2))

		# fixed angle
		R2 = np.dot(self.rotation("y",theta2),self.rotation("x",-np.pi/2))
		P2 = self.prismatic(0,0,self.l1)

		R3 = self.rotation("y",-np.pi/2)
		P3 = self.prismatic(-self.l2-d,0,0)

		T_WA = self.transformer(R1,P1)
		T_AB = self.transformer(R2,P2)
		T_BC = self.transformer(R3,P3) 

		T_forward = np.eye(4)
		for i in [T_WA,T_AB,T_BC]:
			T_forward = np.dot(T_forward,i)
		
		coord_world = np.dot(T_forward,coord_tip)
		return coord_world

	def inverse(self,coord_tip,status):
		coord_world = self.forward(coord_tip,status)
		x = coord_world[0][0] # mm
		y = coord_world[1][0] # mm
		z = coord_world[2][0] # mm
		theta1 = np.arctan2(y,x)
		if theta1 > 0:
			theta1 -= np.pi
		elif theta1 < 0:
			theta1 += np.pi
		theta2 = np.arctan2((z-self.l1),((x**2+y**2)**0.5))
		d = ((x**2+y**2+(z-self.l1)**2)**0.5 - self.l2)/1000.0 # mm to m
		rcm_target_status = [theta1, theta2, d]
		return rcm_target_status


	def transformer(self, R, P):
		T = np.concatenate((R,P),axis= 1)
		T = np.concatenate((T,np.array([[0,0,0,1]])),axis= 0)
		return T

	def rotation(self, axis, deg=0):
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
		else:
			R = np.eye(3)
		return R

	def prismatic(self, x, y, z):
		p = np.array([[x],[y],[z]])
		return p





