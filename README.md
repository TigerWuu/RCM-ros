# RCM-ros
RCM mechanism with gazebo simulation
## Instlal ROS joystick_driver
  *
## Quick Start
  * create ws and source directory
        
        mkdir -p /RCM_ws/src
      
  * Clone the package into the source directory
  
        cd ~/RCM/src && git clone https://github.com/TigerWuu/RCM-ros.git
      
  * build the package
  
        cd ~/RCM_ws && catkin_make
        
  * add the environment variable

        source ~/RCM_ws/src/devel/setup.bash
    
  * launch all
  
        roslaunch auto All.launch
