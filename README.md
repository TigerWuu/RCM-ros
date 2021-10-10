# RCM-ros
RCM mechanism with gazebo simulation

## Quick Start
  * create ws and source directory
        mkdir -p /RCM_ws/src
      
  * Clone the package into the source directory
  
        cd ~/RCM/src && git clone https://github.com/TigerWuu/RCM-ros.git
      
  * build the package
  
        cd ~/RCM_ws && catkin_make
    
  * done
  
        roslaunch auto All.launch
