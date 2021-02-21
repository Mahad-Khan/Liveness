import random 
import cv2
import imutils
import f_liveness_detection 
import questions


def show_image(cam,text,color = (0,0,255)):
    im = imutils.resize(im, width=720)
    #im = cv2.flip(im, 1)
    cv2.putText(im,text,(10,50),cv2.FONT_HERSHEY_COMPLEX,1,color,2)
    return im


def check_live():
    # parameters 
    COUNTER, TOTAL = 0,0
    counter_ok_questions = 0
    counter_ok_consecutives = 0
    limit_consecutives = 3
    limit_questions = 4
    counter_try = 0
    limit_try = 50 
    #cv2.namedWindow('liveness_detection')
    #cam = cv2.VideoCapture(0)
    cam = cv2.VideoCapture('/home/mahad/Tezaract/multiple_liveness/Server/blue/api/notsmile.mp4')
    question = questions.question_bank(0)#index_question)
    print(question)
    count=0
    #im = show_image(cam,question)

    for i_try in range(limit_try):
        cam.set(1, count)
        count += 30 # i.e. at 30 fps, this advances one second
        ret, im = cam.read()
        if im is None:
            break
        im = imutils.resize(im, width=720)
        im = cv2.flip(im, 1)
        TOTAL_0 = TOTAL
        out_model = f_liveness_detection.detect_liveness(im,COUNTER,TOTAL_0)
        TOTAL = out_model['total_blinks']
        COUNTER = out_model['count_blinks_consecutives']
        #dif_blink = TOTAL-TOTAL_0
        #if dif_blink > 0:
         #   blinks_up = 1
        #else:
        #    blinks_up = 0
        blinks_up = 1
        challenge_res = questions.challenge_result(question, out_model,blinks_up)

        #im = show_image(cam,question)
        #cv2.imshow('liveness_detection',im)
        #if cv2.waitKey(1) &0xFF == ord('q'):
            #   break 

        if challenge_res == "pass":
            #im = show_image(cam,question+" : ok")
            print('Pass')
            
            #cv2.imshow('liveness_detection',im)
            #if cv2.waitKey(1) &0xFF == ord('q'):
                #   break

            # counter_ok_consecutives += 1
            # if counter_ok_consecutives == limit_consecutives:
            #     counter_ok_questions += 1
            #     counter_try = 0
            #     counter_ok_consecutives = 0
            #     break
            # else:
            #     continue

        elif challenge_res == "fail":
            print('Fail')
            counter_try += 1
            #show_image(cam,question+" : fail")
        elif i_try == limit_try-1:
            break
            

    # if counter_ok_questions ==  limit_questions:
    #     while True:
    #         im = show_image(cam,"LIFENESS SUCCESSFUL",color = (0,255,0))
    #         #cv2.imshow('liveness_detection',im)
    #         #if cv2.waitKey(1) &0xFF == ord('q'):
    #             #   break
    
    # elif i_try == limit_try-1:
    #     while True:
    #         im = show_image(cam,"LIFENESS FAIL")
    #         #cv2.imshow('liveness_detection',im)
    #         #if cv2.waitKey(1) &0xFF == ord('q'):
    #             #   break
    #     break 

    # else:
    #     continue
