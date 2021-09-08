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

import rospy 
from std_msgs.msg import Float64MultiArray, String
from gazebo_msgs.srv import GetJointProperties
import numpy as np 
from robot import RCM

def coordinate_callback(msg):
	tip_coord = msg.data
	tip_coord = np.asarray(tip_coord).reshape((4,1))

	rospy.wait_for_service('/gazebo/get_joint_properties')
	try:
		rcm_current_joint_status = rospy.ServiceProxy('/gazebo/get_joint_properties', GetJointProperties)
		Link1_joint = rcm_current_joint_status("Link1_joint").position[0]
		Link2_1_joint = rcm_current_joint_status("Link2_1_joint").position[0]
		Link_E_joint = rcm_current_joint_status("Link_E_joint").position[0]
	except rospy.ServiceException as e:
		print(e)

	### for test
	# theta1 = 0
	# theta2 = 0
	# d = 0
	# current_joint_status = [theta1,theta2,d]

	# uu = [Link1_joint*180/np.pi, Link2_1_joint*180/np.pi, Link_E_joint]
	# print(uu)

	current_joint_status = [Link1_joint, Link2_1_joint, Link_E_joint]
	print(current_joint_status)

	rcm = RCM(324,25.87)
	world_coord = rcm.forward(tip_coord,current_joint_status)
	rcm_target_status = rcm.inverse(tip_coord,current_joint_status)
	print(rcm_target_status)


	world_coord = Float64MultiArray(data = world_coord)
	rcm_target_status = Float64MultiArray(data = rcm_target_status)
	pub_world_coord.publish(world_coord)
	pub_target_status.publish(rcm_target_status)


if __name__ == '__main__':
	rospy.init_node('auto')
	pub_world_coord = rospy.Publisher("/world_coordinate", Float64MultiArray,queue_size=1)
	pub_target_status = rospy.Publisher("/rcm_1_5/pos_cmd", Float64MultiArray,queue_size=1)
	rospy.Subscriber("/tip_coordinate", Float64MultiArray, coordinate_callback,queue_size=1, buff_size=52428800)
	rospy.spin()
