#!/usr/bin/env python

import rospy 
from std_msgs.msg import Float64MultiArray, String
from sensor_msgs.msg import Joy
import numpy as np 
import kinematics as k

def coordinate_callback(msg):
    tip_coord = msg.data
    tip_coord = tip_coord.reshape((3,1))
    theta1 = np.pi
    theta2 = np.pi
    d = 10
    D = -25.87-d
    T_WA = k.transformer(k.rotation("z",theta1),k.prismatic(0,0,0))
    T_AB = k.transformer(np.dot(k.rotation("x",-1/2*np.pi),k.rotation("z",theta2)),k.prismatic(0,0,324))
    T_BC = k.transformer(k.rotation("y",-1/2*np.pi),k.prismatic(D,0,0))
    
    world_coord = k.forward([T_WA,T_AB,T_BC],tip_coord)


if __name__ == '__main__':
    rospy.init_node('kinematic')
    pub_world_coord = rospy.Publisher("/world_coordinate", Float64MultiArray,queue_size=1)
    rospy.Subscriber("/tip_coordinate", Float64MultiArray, coordinate_callback,queue_size=1, buff_size=52428800)
    rospy.spin()
