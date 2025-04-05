import cv2
import mediapipe as mp
import numpy as np
import math
import tensorflow as tf
import os

def thumb_judge(hand_point):
    if(hand_point[17][0]>hand_point[4][0] and (hand_point[4][0]>hand_point[3][0] or ((hand_point[3][0]-hand_point[4][0])<20) and hand_point[4][0]<hand_point[3][0])):
        return True
    elif (hand_point[17][0]<hand_point[4][0] and (hand_point[4][0]<hand_point[3][0] or ((hand_point[4][0]-hand_point[3][0])<20) and hand_point[4][0]>hand_point[3][0])):
        return True
    else:
        return False


def vector_2d_angle(v1, v2):
    #內積求cos
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle = 180
    return angle

def hand_angle(hand_):
    angle_list = []
    count=0
    # pointer angle
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    for i in range(8,21,4):
        if(hand_[i][1]<=hand_[i-3][1]):
            count+=1
    angle_list.append(count)
    return angle_list

def combination_draw(img1,img2):
    x=img1.shape[1]
    y=img1.shape[0]
    middle=int(x/2-img2.shape[1]/2)
    img1[y-img2.shape[1]:y,middle:middle+img2.shape[0]]=img2[:,:]
    return img1


#arr[0]=X  arr[1]=Y  arr[2]=enemy_no
def enemy_down(img,arr,en):
    black=np.zeros((50,50,3),np.uint8)
    for i in arr:
        img[i[1]:i[1]+50,i[0]:i[0]+50,:]=black[:,:,:]
        i[1]+=50
        img[i[1]:i[1]+50,i[0]:i[0]+50,:]=en[i[2]][:,:,:]

#change heart
def loss_life(img,num,heart):
    if num==1:
        img[5:45,455:495]=(0,0,0)
        img[5:45,455:495,:]=heart[:,:,:]
    elif num==2:
        img[5:45,505:545]=(0,0,0)
        img[5:45,505:545,:]=heart[:,:,:]
    return img

np.set_printoptions(suppress=True)
mp_hands = mp.solutions.hands.Hands(max_num_hands=1, model_complexity=1,min_detection_confidence=0.7,min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
handList=[]
draw_copy=[]
gesture_angle=[]
coordinate=[]
enemy=[]
draw_judge=False
copy_gesture_angle=[[0,0],[0,0]]
cap = cv2.VideoCapture(0)
model = tf.keras.models.load_model('keras_model.h5', compile=False)
class_names = open("labels.txt", "r").readlines()
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)  
hand1=cv2.imread("hand_finger.png")
hand2=cv2.imread("hand_finger1.png")
black_heart=cv2.imread("black_heart.png")
red_heart=cv2.imread("red_heart.png")
count=0
score=0
loss_life_count=0
speed=100        #more low more hard

for filename in os.listdir("./enemy"):
    img = cv2.imread("./enemy/"+filename)
    img=cv2.resize(img,(50,50))
    enemy.append(img)
    
#interface   600*800
desktop=np.zeros((800,600,3),np.uint8)

n1=np.zeros((150,100,3),np.uint8)
n2=np.zeros((150,100,3),np.uint8)
hand1=cv2.resize(hand1,(100,150))
hand2=cv2.resize(hand2,(100,150))
n1[:,:,:]=hand1[:,:,:]
n2[:,:,:]=hand2[:,:,:]

desktop[580:730,50:150,:]=n1[:,:,:]
desktop[580:730,450:550,:]=n2[:,:,:]

cv2.putText(desktop, "Draw hand", (50,760), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
cv2.putText(desktop, "Finish hand", (440,760), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

#life heart
black_heart=cv2.resize(black_heart,(40,40))
red_heart=cv2.resize(red_heart,(40,40))
for i in range(0,3):
    desktop[5:45,455+(i*50):455+(i*50)+40,:]=red_heart[:,:,:]

#down line
for i in range(0,601,18):
    if i+14>=600:
        cv2.line(desktop,(i,550),(600,550),(255,255,255),3)
    else:
        cv2.line(desktop,(i,550),(i+9,550),(255,255,255),3)

#up line      
for i in range(0,601,18):
    if i+14>=600:
        cv2.line(desktop,(i,50),(600,50),(255,255,255),3)
    else:
        cv2.line(desktop,(i,50),(i+9,50),(255,255,255),3)


if cap.isOpened():
    ret, frame = cap.read()
    frame_x=frame.shape[1]
    frame_y=frame.shape[0]

draw=np.zeros((frame_y,frame_x,3),np.uint8)
draw_copy=cv2.resize(draw,(224,224))

while cap.isOpened():
    #enemy timer
    count+=1
    if count==speed:
        count=0
        if coordinate:
            if coordinate[0][1]+50>500:
                desktop[coordinate[0][1]:coordinate[0][1]+50,coordinate[0][0]:coordinate[0][0]+50]=(0,0,0)
                coordinate.pop(0)
                loss_life_count+=1
                if loss_life_count==3:
                    desktop[:,:]=(0,0,0)
                    cv2.putText(desktop, "GAME OVER", (100,350), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 4)
                    cv2.putText(desktop, "Score:"+str(score), (200,500), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                    cv2.imshow("Index finger magic",desktop)
                    cv2.destroyWindow('camera')
                    rekey=cv2.waitKey(0)
                    break
                else:
                    desktop=loss_life(desktop,loss_life_count,black_heart)
            enemy_down(desktop,coordinate,enemy)
        random_x=np.random.randint(50,550)
        enemy_no=np.random.randint(0,8)
        coordinate.append([random_x,70,enemy_no])
        desktop[70:120,random_x:random_x+50,:]=enemy[enemy_no][:,:,:]

    #hand_read
    ret, frame = cap.read()
    if not ret:
        continue
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:         
            handLandMark_list=[]
            for i,hp in enumerate( hand_landmarks.landmark):
                hp_x=hp.x*frame_x
                hp_y=hp.y*frame_y
                handLandMark_list.append([hp_x,hp_y])

            #for cal pointer finger
            if gesture_angle:
                copy_gesture_angle[1]=copy_gesture_angle[0]
                copy_gesture_angle[0]=gesture_angle
            gesture_angle=hand_angle(handLandMark_list)
            
            #write
            if thumb_judge(handLandMark_list) and gesture_angle[1]==1 and gesture_angle[0]<60:
                if copy_gesture_angle[0][1]==1 and copy_gesture_angle[0][0]<80:
                    if copy_gesture_angle[1][1]==1 and copy_gesture_angle[1][0]<80:   
                        handList.append([hand_landmarks.landmark[8].x,hand_landmarks.landmark[8].y])
                        dl = len(handList)
                        if dl>1:
                            dx1 = int(handList[dl-2][0]*frame_x)
                            dy1 = int(handList[dl-2][1]*frame_y)
                            dx2 = int(handList[dl-1][0]*frame_x)
                            dy2 = int(handList[dl-1][1]*frame_y)
                            cv2.line(draw,(frame_x-dx1,dy1),(frame_x-dx2,dy2),(0,255,0),5)
                            cv2.circle(frame,(int(handLandMark_list[8][0]),int(handLandMark_list[8][1])),5,(0,255,0),-1)
                            draw_judge=True
            #clean & predict
            elif thumb_judge(handLandMark_list) and gesture_angle[1]==0 and gesture_angle[0]>60:
                if copy_gesture_angle[0][1]==0:
                    if copy_gesture_angle[1][1]==0:
                        handList=[]
                        if draw_judge:
                            draw_copy=cv2.resize(draw,(224,224),interpolation=cv2.INTER_AREA)
                            image_array = np.asarray(draw_copy,dtype=np.float32).reshape(1, 224, 224, 3)
                            image_array = (image_array / 127.5) - 1
                            prediction = model.predict(image_array)
                            index = np.argmax(prediction)

                            #if there are more shapes , index need to update
                            if (prediction[0][index]>=0.7 and index!=8 and coordinate) or (prediction[0][index]>=0.5 and index==2 and coordinate):  
                                for i,j in enumerate (coordinate):
                                    if j[2]==index:
                                        score+=1
                                        desktop[coordinate[i][1]:coordinate[i][1]+50,coordinate[i][0]:coordinate[i][0]+50]=(0,0,0)
                                        coordinate.pop(i)
                                        break
                            
                            class_name = class_names[index]
                            #print("Class:", class_name[2:], end="")
                            #print("Confidence Score:", prediction[0][index])
                            draw=np.zeros((frame_y,frame_x,3),np.uint8)
                            draw_judge=False

    
    desktop[0:49,0:200]=(0,0,0)
    cv2.putText(desktop, "Score:"+str(score), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    draw_copy=cv2.resize(draw,(224,224))
    desktop=combination_draw(desktop,draw_copy)
    cv2.imshow("Index finger magic",desktop)
    cv2.imshow("camera",frame)
    key=cv2.waitKey(1)
    if key== ord('q') or key== ord('Q'):
        break

  
cap.release()
cv2.destroyAllWindows()