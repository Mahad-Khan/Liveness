from flask import Blueprint,jsonify, request
from flask_restful import Api,Resource
from werkzeug.utils import secure_filename
import urllib
import cv2
import requests
import sys
import os
import json
import imutils

import numpy as np
import dlib
from PIL import Image
from scipy import io
import imageio
### change the "/" to "\\" if you are windows user ###
dirname = os.path.dirname(os.path.abspath(__file__))


path = dirname
sys.path.append(path)
print(path)
dirname_list = dirname.split("/")[:-2]
main_video_dirname = "/".join(dirname_list)
print(main_video_dirname)

from face_anti_spoofing1 import check_gesture
from crop_file import crop_save
from id_generator import id_generator
from face_matching import verification

mod = Blueprint('api',__name__)
api = Api(mod)

path_frame=path+'/frame-database/'
path_id=path+'/id-database/'


class Get_Video_File(Resource):
    def post(self):
        try:
            my_dict = dict()
            #######################Read Gesture 01 and Video of Gesture 01######################
            gesture_01 = request.form.get('gesture1')
            video_01 = request.files['video1'].read()
            f = open('video1.mp4', 'wb')
            f.write(video_01)
            f.close()
            cam_01 = cv2.VideoCapture('video1.mp4')
            print(gesture_01)
            ##########################Gesture Verification Function############################
            '''
            - input : cam Video
            - output : 0 or 1 (If Gesture Found than function returns 1 else 0 )
            {'gesture_name:1'}
            '''
            result1=check_gesture(cam_01,gesture_01)
            print('Check',result1)
            my_dict[gesture_01] = result1
            #exit()
            #######################Read Gesture 02 and Video of Gesture 02######################
            gesture_02 = request.form.get('gesture2')
            video_02 = request.files['video2'].read()
            f = open('video2.mp4', 'wb')
            f.write(video_02)
            f.close()
            cam_02 = cv2.VideoCapture('video2.mp4')
            print(gesture_02)
            ##########################Gesture Verification Function############################
            '''
            - input : cam Video
            - output : 0 or 1 (If Gesture Found than function returns 1 else 0 )
            '''
            result2=check_gesture(cam_02,gesture_02)
            print('Check',result2)
            my_dict[gesture_02] = result2
            #######################Read Gesture 03 and Video of Gesture 03######################
            gesture_03 = request.form.get('gesture3')
            video_03 = request.files['video3'].read()
            f = open('video3.mp4', 'wb')
            f.write(video_03)
            f.close()
            cam_03 = cv2.VideoCapture('video3.mp4')
            print(gesture_03)
            ##########################Gesture Verification Function############################
            '''
            - input : cam Video
            - output : 0 or 1 (If Gesture Found than function returns 1 else 0 )
            '''
            result3=check_gesture(cam_03,gesture_03)
            print('Check',result3)
            my_dict[gesture_03] = result3
            #######################Read Gesture 04 and Video of Gesture 04######################
            gesture_04 = request.form.get('gesture4')
            video_04 = request.files['video4'].read()
            f = open('video4.mp4', 'wb')
            f.write(video_04)
            f.close()
            cam_04 = cv2.VideoCapture('video4.mp4')
            print(gesture_04)
            ##########################Gesture Verification Function############################
            '''
            - input : cam Video
            - output : 0 or 1 (If Gesture Found than function returns 1 else 0 )
            '''
            result4=check_gesture(cam_04,gesture_04)
            print('Check',result4)
            my_dict[gesture_04] = result4

            
            ################################ Save  Frame ##########################
            
            ret, frame = cam_04.read()
            image = imutils.resize(frame,height=280, width=280)
            frame_id=request.form.get('id')
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            crop_save(image,frame_id,path_frame)
            #cv2.imwrite(path+'/frame-database/'+frame_id+'.jpg',image)
            #image = cv2.flip(image, 1)
            # img=frame.resize((280,280), Image.ANTIALIAS)
            # img.save(path+'/frame-databse/framepic.jpg')


            ############################## VERIFICATION #################################

            
            img1_path=path_id+frame_id+'.jpg'
            img2_path=path_frame+frame_id+'.jpg'
            verif_result=verification(img1_path,img2_path)

        

            #Delete mp4 bytes files
            filelist = [ f for f in os.listdir(main_video_dirname) if f.endswith(".mp4") ]
          
            for f in filelist:
                os.remove(os.path.join(main_video_dirname, f))
            #Output Json
            gestures=[gesture_01,gesture_02,gesture_03,gesture_04]
            reusults=[result1,result2,result3,result4]
            pass_list=[True for i in reusults if i=='pass']
            
            print("Pass List: ",pass_list)
            num_of_success_gest=sum(pass_list)
            print(num_of_success_gest)
            #if len(num_of_success_gest)>=3:
            liveness_status = None
            gesture_fail_list = list()
            if num_of_success_gest==4:
                print('Liveness Test Pass')
                liveness_status = "pass"
                gesture_fail_list = []
            else:
                print('Liveness Test Fail')
                liveness_status = "fail"
                for i in range(len(reusults)):
                    if reusults[i] == "fail":
                        print("Failed Here -> "+ "" + gestures[i] + " -> " + reusults[i])
                        gesture_fail_list.append(gestures[i])
                    else:
                        pass


            print(my_dict)
            dic = {"status":200,"msg":"ok","liveness_status":liveness_status,
                   "gesture_fail_list":gesture_fail_list,'verification':verif_result}
            
            return jsonify(dic)
        except Exception as e:
            dic = {"status":444,"msg":"faliure","reason":str(e)}
            return jsonify(dic)


class Get_image_for_id(Resource):
    def post(self):
        image = request.files['image'].read()
        npimg = np.fromstring(image, np.uint8)
        img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        id=id_generator()
        crop_save(img,id,path_id)
        

        dic = {"status":200,"id":id}
        return jsonify(dic)



api.add_resource(Get_Video_File, "/get_video_file")
api.add_resource(Get_image_for_id,"/get_image_for_id")