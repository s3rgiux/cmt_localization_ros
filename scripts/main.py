#!/usr/bin/env python
from __future__ import print_function
import roslib
#roslib.load_manifest('cmt')
import sys
import rospy
import cv2
from std_msgs.msg import String
from std_msgs.msg import Float32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from numpy import empty, nan
import os
import sys
import time
import CMT
import numpy as np
import util
import math
import tf
# Messages
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Quaternion, Vector3

def rigid_transform_3D(A, B):
  #print 'Llamado'
  assert len(A) == len(B)

  N = A.shape[0]; # total points

  centroid_A = np.mean(A, axis=0)
  centroid_B = np.mean(B, axis=0)
  
  # centre the points
  AA = A - np.tile(centroid_A, (N, 1))
  BB = B - np.tile(centroid_B, (N, 1))

  # dot is matrix multiplication for array
  H = np.transpose(AA)* BB

  U, S, Vt = np.linalg.svd(H)

  R = Vt.T * U.T

  # special reflection case
  if np.linalg.det(R) < 0:
     #print "Reflection detected"
     Vt[2,:] *= -1
     R = Vt.T * U.T

  t = -R*centroid_A.T + centroid_B.T

  #print t

  return R, t

# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = Rt*R
    print(shouldBeIdentity)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

def rotationMatrixToEulerAngles(R) :
 
    #assert(isRotationMatrix(R))
     
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
     
    singular = sy < 1e-6
 
    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0
 
    return np.array([x, y, z])

class image_converter:


  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_cmt",Image,queue_size=1)
    self.vis_odo_pub = rospy.Publisher("visual_odometry",Odometry,queue_size=1)
    self.bridge = CvBridge()
    #self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)
    self.image_sub = rospy.Subscriber("/ocam/image_raw",Image,self.callback,queue_size=1)
    self.yaw_sub = rospy.Subscriber( "model_car/yaw2", Float32,self.headingcallback,queue_size=1)
    #self.odom_sub = rospy.Subscriber( "odom", Float32,self.h,queue_size=1)
    #self.image_sub = rospy.Subscriber("/usb2_cam/image_rect_color",Image,self.callback)
    self.CRT = CMT.CMT()
    


    self.CRT.estimate_scale = 'estimate_scale'
    self.CRT.estimate_rotation = 'estimate_rotation'
    self.pause_time = 10
    ###########################Primer Region
    #im0 = cv2.imread('./frame_cuadri_1500.jpg', flags=cv2.IMREAD_GRAYSCALE)
    #im0 = cv2.imread('./frame_cap_16.jpg', flags=cv2.IMREAD_GRAYSCALE)
    im0 = cv2.imread('./frame_cap_11.jpg', flags=cv2.IMREAD_GRAYSCALE)
    #im0 = cv2.imread('./frame_fisica3.jpg', flags=cv2.IMREAD_GRAYSCALE)
    #im0 = cv2.imread('./frame_cap_16.jpg', flags=cv2.IMREAD_GRAYSCALE)
    #im0 = cv2.imread('./frame_cap_noche.jpg', flags=cv2.IMREAD_GRAYSCALE)
    #im0 = cv2.imread('./frame_cap3.jpg', flags=cv2.IMREAD_GRAYSCALE)#flags=cv2.IMREAD_GRAYSCALE)
    #im0 = cv2.imread('/home/sergio/catikin_ws_user/src/cmt/scripts/frame.jpg', flags=cv2.IMREAD_COLOR)
    #im0 = cv2.imread('/home/sergio/catikin_ws_user/src/cmt/scripts/frame.jpg',flags=cv2.IMREAD_GRAYSCALE)
    #cv2.imshow('im0', im0)
    #im_gray0 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)
    im_gray0=im0
    #print(np.size(im_gray0))
    #im_gray0=cv2.blur(im0,(3,3))
    #cv2.line(im_gray0, (70,0), (70,300), (0, 0, 0), 150)
    #cv2.line(im_gray0, (490,0), (490,300), (0, 0, 0), 150)
    #im_gray0=cv2.resize(im0, (360, 240))
    #im_draw = np.copy(im0)
    print('Selecciona Primer Region')
    #tl=(84, 55) #talvez
    #br=(557, 307#tal vez
    #tl=(68, 68) 
    #br=(544, 316)
    #tl=(35,35)
    #bl=(605,325)
    #tl=(78, 59) #ultimos con156kp
    #br=(553, 297)#uktimos con 156kp
    tl=(73, 56) #labo umi
    br=(449, 244)#labo umi
    
    #tl=(88, 58) #camaras labo
    #br=(429, 240)#camaras labo
    #tl=(93, 61) #camaras labo nuevo 
    #br=(436, 241)#labo camaras nuevo
    # tl=(85, 59)#last camrasa
    # br=(428, 239)#lascamaras
    # #tl=(166, 64)
    # #br=(348, 237)
    # #(84, 63) (429, 237)
    # #tl=(87, 57)#camaras
    # #br= (426, 234)#camaras
    # tl=(87, 57)#camaras
    # br=(326, 154)#camaras
    # tl=(59, 44)#camaras peque
    # br= (300, 195)#camaras peque
    # tl=(128, 25) 
    # br=(394, 278)

    # ##cuadrilatero
    # #tl=(157,6)
    # #br=(408,257)
    # tl=(154,21)#55)
    # br=(392,259)
    # #tl=(40+20,27+20)
    # #br=(269-20, 256-20)
    # tl=(40+10,27+10)
    # br=(269-10, 256-10)
    # tl=(320-146,180-146)
    # br=(320+146,180+146)
    #(158, 14) (392, 261)


    ##fisica
    #tl=(118, 54)
    #br=(348, 250)
    #(tl, br) = util.get_rect(im_gray0)
    print('usando %i, %i como init bb', tl, br)
    self.CRT.initialise(im_gray0, tl, br)
    print('Num keypoint init',self.CRT.num_initial_keypoints)
    self.frame = 1
    self.conta=0


    self.frame_id = 'visual_odometry'
    self.child_frame_id = 'base_link2'
    self.msg = Odometry()
    # Covariance
    #P = np.mat(np.diag([0.0]*3))
    
  def headingcallback(self,dat):
      self.yaw=dat.data

  def callback(self,data):
    try:
        tic = time.time()
        new_yaw=self.yaw
        im_gray = self.bridge.imgmsg_to_cv2(data, "mono8")
        #print(np.size(im_gray))
        # Read image
        #status, im = cap.read()
        #im=cv_image
        #im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        #im_gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        #im_draw = np.copy(cv_image)
        #cv2.line(im_gray, (70,0), (70,300), (0, 0, 0), 150)
        #cv2.line(im_gray, (490,0), (490,300), (0, 0, 0), 150)
        #im_gray=cv2.blur(im_gray,(3,3))
        #im_gray=cv2.resize(im_gray, (360, 240))
        self.CRT.process_frame(im_gray)
        
	# Remember image
        im_prev = im_gray
        # Display results
        print(self.CRT.active_keypoints.shape[0])
        # Draw updated estimate
        if self.CRT.has_result and self.CRT.active_keypoints.shape[0]>self.CRT.num_initial_keypoints*0.3:#*0.37:

          #cv2.line(im_gray, self.CRT.tl, self.CRT.tr, (255, 0, 0), 4)
          #cv2.line(im_gray, self.CRT.tr, self.CRT.br, (255, 0, 0), 4)
          #cv2.line(im_gray, self.CRT.br, self.CRT.bl, (255, 0, 0), 4)
          #cv2.line(im_gray, self.CRT.bl, self.CRT.tl, (255, 0, 0), 4)
          #font = cv2.FONT_HERSHEY_SIMPLEX
          #cv2.putText(im_gray,'1',(self.CRT.tl[0],self.CRT.tl[1]), font, 3, (200,255,155), 7, cv2.CV_AA)
          #cv2.putText(im_gray,'2',(self.CRT.tr[0],self.CRT.tr[1]), font, 3, (200,255,155), 7, cv2.CV_AA)
          #tl=(68, 68) #600cm=476pix
          #br=(544, 316)#300cm=248
          #gk=1.2605042
          gk=1.59574468#//labo
          #gk=1.12781955
          #gk=6.41434
          #gk=7.892156
          #gk=6.76470588
          #gk=5.55172414
          #gk=2.8043478261
          offs_x=256#320
          offs_y=144#180
          p1=[(self.CRT.tl[0]-offs_x)*gk,(self.CRT.tl[1]-offs_y)*gk,0]
          p2=[(self.CRT.tr[0]-offs_x)*gk,(self.CRT.tr[1]-offs_y)*gk,0]
          p3=[(self.CRT.bl[0]-offs_x)*gk, (self.CRT.bl[1]-offs_y)*gk,0]
          p4=[(self.CRT.br[0]-offs_x)*gk, (self.CRT.br[1]-offs_y)*gk,0]

          MCI=np.mat([p1,p2,p3,p4])
          MCR=np.mat([[-300,150,0],[300,150,0],[-300,-150,0],[300,-150,0]])
          #MCR=np.mat([[-322.5,267.5,0],[322.5,267.5,0],[-322.1,-267.5,0],[322,-267.5,0]])
          #MCR=np.mat([[-270,210,0],[270,210,0],[-270,-210,0],[270,-210,0]])
          #MCR=np.mat([[-150,150,0],[150,150,0],[-150,-150,0],[150,-150,0]])
          #MCR=np.mat([[-805+20*gk,805-20*gk,0],[805-20*gk,805-20*gk,0],[-805+20*gk,-805+20*gk,0],[805-20*gk,-805+20*gk,0]])
          #MCR=np.mat([[-805+10*gk,805-10*gk,0],[805-10*gk,805-10*gk,0],[-805+10*gk,-805+10*gk,0],[805-10*gk,-805+10*gk,0]])
          #MCR=np.mat([[-805,805,0],[805,805,0],[-805,-805,0],[805,-805,0]])
          ret_R, ret_t = rigid_transform_3D(MCI, MCR) 
          vec_r=rotationMatrixToEulerAngles(ret_R)
          try:
            #resized_image = cv2.resize(image, (100, 50)) 
            #self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv2.resize(im_gray, (100, 55)) , "mono8"))
            self.msg.header.stamp = rospy.Time.now()
            self.msg.header.frame_id = self.frame_id # i.e. '/odom'
            self.msg.child_frame_id = self.child_frame_id # i.e. '/base_footprint'

            self.msg.pose.pose.position = Point(ret_t[0,0]/100,ret_t[1,0]/100, vec_r[2]*180/3.14159)#ret_t[2,0]/100)
            q = tf.transformations.quaternion_from_euler(0, 0, vec_r[2])
            self.msg.pose.pose.orientation = Quaternion(*q)
            # Publish odometry message
            dif=(vec_r[2]*180/3.141)-new_yaw

            if dif>180:
              dif=dif-360
            
            elif dif<-180:
              dif=dif+360

            self.msg.twist.twist.angular=Vector3(0,0,dif)
            
            self.vis_odo_pub.publish(self.msg)
          except CvBridgeError as e:
            print(e)

        self.frame += 1
        
      # Also publish tf if necessary
      #if self.publish_odom_tf:
      #    self.tf_br.sendTransform(pos, ori, msg.header.stamp, msg.child_frame_id, msg.header.frame_id)
        #publish_odom()
        toc = time.time()
        print(1000 * (toc - tic))
        #print(ret_t[0,0],)
        #print(ret_t[0,0],",",ret_t[1,0],",",vec_r[2]*180/3.1416,",",1000 * (toc - tic))
        #print(vec_t[2]*180/3.1416)
        #print(ret_t[0][0],",",ret_t[0][1],",",vec_t[0][2]*180/3.1416)
        #print(ret_t[0][0],",",ret_t[0][1],",",vec_t[2]*180/3.1416)
        #print('P',w[1])
        #print('P',w[2])
        

      
    except CvBridgeError as e:
      print(e)

    

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
