import random 
import cv2
import imutils
import f_liveness_detection 
import questions

# cv2.namedWindow('liveness_detection')
# cam = cv2.VideoCapture(0)

def check_gesture(cam,question):
    print(f"checking {question}")
    # parameters 
    COUNTER, TOTAL = 0,0
    counter_ok_questions = 0
    counter_ok_consecutives = 0
    limit_consecutives = 2
    #limit_questions = 4
    counter_try = 0
    limit_try = 50 
    return_ans='fail'


    count=0
    if question=='blink eyes':
        num=3
    else:
       num=30 
    for i_try in range(limit_try):
        cam.set(1, count)
        ret, im = cam.read()
        count += num # i.e. at 30 fps, this advances one second

        
        if im is None:
            return_ans='fail'
            return return_ans
            break
        im = imutils.resize(im, width=720)
        im = cv2.flip(im, 1)

        TOTAL_0 = TOTAL
        out_model = f_liveness_detection.detect_liveness(im,COUNTER,TOTAL_0)
        TOTAL = out_model['total_blinks']
        COUNTER = out_model['count_blinks_consecutives']
        dif_blink = TOTAL-TOTAL_0
        if dif_blink > 0:
            blinks_up = 1
        else:
            blinks_up = 0

        challenge_res = questions.challenge_result(question, out_model,blinks_up)

        if challenge_res == "pass":
            #print('pass')
            counter_ok_consecutives += 1
            if counter_ok_consecutives == limit_consecutives:
                counter_ok_questions += 1
                counter_try = 0
                counter_ok_consecutives = 0
                #return_results[i_questions]='pass'
                return_ans='pass'
                return return_ans
            else:
                continue

        elif challenge_res == "fail":
            counter_try += 1

        elif i_try == limit_try-1:
            return return_ans
            
  