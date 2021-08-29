#!/usr/bin/env python

import rospy 
from std_msgs.msg import Float64MultiArray, String
import numpy as np 
from robot import RCM

def coordinate_callback(msg):
	# mm
    tip_coord = msg.data
    tip_coord = np.asarray(tip_coord).reshape((4,1))

    theta1 = 0.25*np.pi
    theta2 = 0.25*np.pi
    d = 10

	rcm_status = [theta1,theta2,d]
    rcm = RCM(324,25.87)
    world_coord = rcm.forward(tip_coord,rcm_status)
    world_coord = Float64MultiArray(data = world_coord)
    pub_world_coord.publish(world_coord)


if __name__ == '__main__':
    rospy.init_node('kinematic')
    pub_world_coord = rospy.Publisher("/world_coordinate", Float64MultiArray,queue_size=1)
    rospy.Subscriber("/tip_coordinate", Float64MultiArray, coordinate_callback,queue_size=1, buff_size=52428800)
    rospy.spin()
