#!/usr/bin/env python
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
from __future__ import print_function
import sys
import rospy
import cv2
import numpy as np

from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String, UInt16, UInt8, Float64MultiArray
from sensor_msgs.msg import Image
from gazebo_msgs.srv import GetJointProperties

x_pixel = 0 
y_pixel = 0
z = 0

class image_converter:
	def __init__(self):
		self.bridge = CvBridge()
		rospy.Subscriber("/camera/color/image_raw",Image,self.color_image_callback)
		rospy.Subscriber("/camera/depth/image_raw",Image,self.depth_image_callback)
		self.pub_tip_coord = rospy.Publisher("/tip_coordinate",Float64MultiArray,queue_size=1)
	
	def color_image_callback(self,data):
		try:
			cv_image_color = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

		cv2.namedWindow("color_image")
		cv2.setMouseCallback('color_image',self.get_camera_coordinate)

		cv2.imshow("color_image",cv_image_color)
		cv2.waitKey(1)

	def depth_image_callback(self,data):
		global x_pixel,y_pixel,z
		try:
			cv_image_depth = self.bridge.imgmsg_to_cv2(data)
		except CvBridgeError as e:
			print(e)
		# print(cv_image_depth[y_pixel][x_pixel])
		z = cv_image_depth[y_pixel][x_pixel] # m

		# cv2.imshow("depth_image", cv_image_depth)
		# key = cv2.waitKey(1)

	def get_camera_coordinate(self,event,x,y,flags,param):
		global x_pixel,y_pixel,z
		if event == cv2.EVENT_LBUTTONDOWN:
			x_pixel = x
			y_pixel = y
			z = z * 1000 # m to mm

			### camera calibration ###
			camera_coord = calibration(x_pixel,y_pixel,z)

			print(camera_coord)
			rospy.wait_for_service('/gazebo/get_joint_properties')
			try:
				rcm_current_joint_status = rospy.ServiceProxy('/gazebo/get_joint_properties', GetJointProperties)
				Link_E_joint = rcm_current_joint_status("Link_E_joint").position[0]*1000 # m to mm 
			except rospy.ServiceException as e:
				print(e)

			# camera_coord = np.array([[0],[0],[0],[1]])

			R = rotation("I")
			P = prismatic(0,-14.61,-54.87-Link_E_joint)
			T_CCa = transformer(R, P)
			tip_coord = np.dot(T_CCa,camera_coord)
			tip_coord = Float64MultiArray(data = tip_coord)
			self.pub_tip_coord.publish(tip_coord)

def calibration(x,y,z):
	# f = 1110.046974
	camera_cx = 640
	camera_cy = 360
	camera_fx = 277 # f/dx
	camera_fy = 277
	cz = z
	cx = (x - camera_cx) * cz / camera_fx
	cy = (y - camera_cy) * cz / camera_fy
	return [[cx],[cy],[cz],[1]]

def transformer(R, P):
	T = np.concatenate((R,P),axis= 1)
	T = np.concatenate((T,np.array([[0,0,0,1]])),axis= 0)
	return T

def rotation(axis, deg=0):
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

def prismatic(x, y, z):
	p = np.array([[x],[y],[z]])
	return p

def main(args):
	ic = image_converter()
	rospy.init_node('UI', anonymous=True, disable_signals=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv)
