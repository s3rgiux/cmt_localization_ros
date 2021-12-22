# CMT Localization

Repository that allows to localizate using any ROI, was designed to operate on indoors just needed to know the size of the region of interest ROI

Link to the article of this repository

https://ieeexplore.ieee.org/document/8540752/


Based on thee algorithm of

https://www.gnebehay.com/cmt/ 

# requires

* Python
* Scipy
* Itertools
* Opencv2

# How to Run

Save the image that conatins the ROI where we want to perform localization.

```
# Clone this workspace on ROS

git clone 

```

install mavros and vrpn
 
```

sudo apt install ros-melodic-mavros ros-melodic-mavros-extras

sudo apt install ros-melodic-vrpn-client-ros 

```

On the file `/src/conversion_coordinates/scripts/conversion_mocap.py` found the line `sub_pose  = rospy.Subscriber("/vrpn_client_node/arana/pose", PoseStamped, self.pose_mocap_callback)` and replace the name `arana` with the name of your rigid body.

# Build

Build workspace with

```
catkin_make
```

#Launch

To launch replace the ip of the next line, with the ip adress of the Motive computer that is stremming over VRPN.

```
 roslaunch control_drone launch_vrpn.launch server:=192.168.11.2:3883
```

# Test

To Test run the script:

```
 rosrun control_drone control_drone_node
```

This dorne wil put PX4 on Offboard mode and could be dangerous so preferently use a RC tranmitter to change the mode just in case








