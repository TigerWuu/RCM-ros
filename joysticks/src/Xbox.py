#! /usr/bin/env python
import rospy
from std_msgs.msg import Float64MultiArray, String
from sensor_msgs.msg import Joy
import os

HZ=10

def joy_remapping(msg):
    rate = rospy.Rate(HZ)
    buttons = msg.buttons
    axes = msg.axes
    # axes = map(lambda x:int(x*100),axes)  
    LRleft,UDleft,LT,LRright,UDright,RT,ckLR,ckUD = axes 
    A,B,X,Y,LB,RB,back,start,power,BSL,BSR=buttons

    # cmd = "%.5f*%.5f*%.5f*%01d" % (UDleft,LRright,UDright,LB)
    cmd = [-UDleft,LRright,UDright,LB]
    cmd = Float64MultiArray(data = cmd)
    pub_joy.publish(cmd)

    rate.sleep()


 
if __name__ == '__main__':
    rospy.init_node('Xbox')
    pub_joy = rospy.Publisher('/rcm_1_5/vel_cmd', Float64MultiArray, queue_size=1)
    rospy.Subscriber("/joy", Joy, joy_remapping, queue_size = 1, buff_size = 52428800)
    rospy.spin()
