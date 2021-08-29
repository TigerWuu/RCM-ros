#!/usr/bin/env python
""" 
-------------------------
Author : Jing-Shiang Wuu, Li-Wei Yang
Date : 2021/7/1
Institution : National Taiwan University 
Department : Bio-Mechatronics Engineering
Status : Senior, Junior
-------------------------
Description:
    It is a program to recieve all the sensor informatoin, including tof(may be deleted), limit switch, button, sticks and image. 
    we plot some important information on the image:
    1. swabing target: there is a tip_offset from the center of image
    2. swabing status: showing the swabing status:searching, swabing in the lower right corner of image
    3. warning information: if the robot touch the limit switch, there is a warning information in the lower right corner of image too.
    the image will zoom in/out if
        * dataz > 21500 ---> zoom in
        * dataz < 18500 ---> zoom out
    the maximum magnification is 10
"""

from __future__ import print_function
import sys
import rospy
import cv2
import numpy as np

from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String, UInt16, UInt8
from sensor_msgs.msg import Image

class image_converter:

    def __init__(self):
        self.bridge = CvBridge()
        rospy.Subscriber("/camera/color/image_raw",Image,self.color_image_callback)
        rospy.Subscriber("/camera/depth/image_raw",Image,self.depth_image_callback)
	
    def color_image_callback(self,data):
        try:
	        cv_image_color = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
            
        cv2.imshow("color_image",cv_image_color)
        cv2.waitKey(1)

    def depth_image_callback(self,data):
        try:
            cv_image_depth = self.bridge.imgmsg_to_cv2(data)
        except CvBridgeError as e:
            print(e)

        cv2.imshow("depth_image", cv_image_depth)
        key = cv2.waitKey(1)

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
