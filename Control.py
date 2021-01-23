'''
Car control functions
Author: Sian
'''
from gopigo import *
import math
import time


#turn on encoders of wheels
enable_encoders()

#global variables
offset = [enc_read(0), enc_read(1)]  # to reset encoder values at start of program to 0
length = 25.5                        # length of GoPiGo in cm
front = 11.5                         # distance from center of wheels to front of GoPiGo
width = 14.5                         # width GoPiGo in cm
wheel_C = 20                         # circumference of wheel in cm
#pos = [0,front,0]                    # current position of GoPiGo wrt front of GoPiGo x,y,rot
L = 0                                # encoder val of left wheel
R = 0                                # encoder val of right wheel

#encoder_to_distance and angle_x may be useful for getting back on course after collision
def encoder_to_distance():
    """
    Converts encoder reading to distance in cm
    """ 
    dis = [0,0] # displacement in cm
    #18 encoder counts per wheel rotation
    dis[0] = (enc_read(0)-offset[0]) * wheel_C/18 #left wheel
    dis[1] = (enc_read(1)-offset[1]) * wheel_C/18 #right wheel
    return(dis)

def angle_x(curr_angle):
    """
    Converts current angular position to an angle wrt x axis for pos update
    """
    if curr_angle <= 3.14/2: #if in 1st quadrant
        quad_angle = curr_angle
    elif curr_angle <= 3.14: #if in 2nd quadrant
        quad_angle = 3.14 - curr_angle
    elif curr_angle <= 3*3.14/2: #if in 3rd quadrant
        quad_angle = curr_angle - 3.14
    else: #if in 4th quadrant
        quad_angle = 2*3.14 - curr_angle
    return(quad_angle)



def const_enc(speed,direction,Kp):
    """
    Ensures that the wheels turn as expected by keeping difference between encoders constant while driving
    """
    
    
    #initialisation of variables
    global L, R, offset
    enc_diff = R-L                    #setpoint to make sure diff between enc is constant
    if direction == 'STRAIGHT':       #ensures diff is 0 for driving straight
        enc_diff = 0
    time.sleep(0.3)
    L = enc_read(0)-offset[0]         #update Left enc count
    R = enc_read(1)-offset[1]         #update Right enc count
    new_diff = R-L

    count = 0 #for TESTINFFFGGGGG
    start = time.perf_counter()

    error = new_diff - enc_diff
    error_prev = 0                    #Previous error 
    t_prev = -100                     #check time with high res timer
    Kp = 41                   #Proportional Gain
    Td = 0.862
    Ti = 100000000000
    I = 0
    
    #Set file heading to P gain
    f = open("ew_P.txt","a")
    f.write("%d \n" % (Kp))
    f.close()

    #while the wheels are not at the same speed implement controller
    while abs(error) > 0:
        
        count = 0.1
        t = time.perf_counter()#check time with high res timer
        
        if t-start > 1.5:
            break
    
        #print and save data
        print(Td,Kp,L,R,error,t-t_prev)
        f = open("ew_P.txt", "a")
        f.write("%d %f %f\n" % (error, t, t_prev))
        f.close()

        # PID control equation
        I = I + (1/Ti)*error*(t-t_prev)
        val = Kp*(error + I + (Td*(error - error_prev)/(t-t_prev)))
        
        #update speed to complete feedback loop
        if speed+val > 0: #wheel should not stop spinning
            set_left_speed(int(round(speed+val)))
        print(speed+val)
        
        time.sleep(0.3)            #short wait time for system to adjust to speed before taking new reading
        offset = [offset[0]+L,offset[1]+R]
        L = enc_read(0)-offset[0]  #reset L to see the new difference between R & L
        R = enc_read(1)-offset[1]
        error = R-L
        t_prev = t

    return(count)

def drive(speed, direction, strength):
    """
    Takes input from APP or Image detection to control motion of leader or follwer (respectively)
    """
    #leader input should come from app 
    #follower input should come from image detection

    #speed to drive fwd
    if speed > 0:
        speed_L = speed
        speed_R = speed - 10
    else:
        speed_L = speed
        speed_R = speed

    #set direction
    fwd()

    #adjust velocity of wheels to steer
    if direction == 'STRAIGHT':
        set_left_speed(speed_L)
        set_right_speed(speed_R)
    elif direction == 'RIGHT':
        speed_L += strength
        set_left_speed(speed_L)
        set_right_speed(speed_R)
    elif direction == 'LEFT':
        speed_L -= strength
        set_left_speed(speed_L)
        set_right_speed(speed_R)

    #strength should be in increments of 10
    return(speed_L)


"""For Joining and Following"""
stop = 0 
pos_car1 = [2,2]
pos_car2 = [1,1]
dx = pos_car1[0] - pos_car2[0]
dy = pos_car1[1] - pos_car2[1]
setpoint = [0,0]
image_frame = [0,0]
Am_leader = 0
found_car = 0
collision = 0


""" initialisation of cars """
#send beacon and triangulate position
#send position to database and car id (car2)
    #append end of platoon list with car id
#check if leader id matches my id
'''
while stop == 0: #(may need to check more often)

    """ for followers """
    if Am_leader == 0:
        """ find car & join platoon """
        #check database for position of car infront (car1)
        #use image detection to search for car infront and update found_car
        while found_car == 0
            #broadcast joining platoon & update platoon list in database  (blink right  LED)
            #rotate theta = arctan(dy/dx) degrees
            #use image detection to search for car infront and update found_car
            while image_frame != setpoint:
                #call image analysis
                #call drive with values from image recognition analysis
                #send beacon and update position
                #call const_enc to ensure wheels turn as intended
                #call image recognition
                
        #check database for car infront(car1)


        #Now car infront should be found and platoon joined with correct car orientation
        """ following in platoon """
        #set speed to speed of car in font
        #call image recognition and image analysis
        #drive with values from analysis (cars 15 cm apart)
        #send beacon and update my position
        #call const_enc() to ensure wheels turn as intended

        """ leaving platoon """
        #if t > 10s && leave == 1:
        #broadcast leaving & update platoon list in database (blink left LED)
        #start driving sequence to leave platoon
        #break

    """ for leaders"""
    else:
        if collision == 0:
            #call drive with commands from app
            #call const_enc() to ensure wheels turn as intended
        else:
            #insert collision avoidance scheme here


            













#testing  drive()
#speed = input("\nEnter speed : ")
#speed = int(speed)
#direction = input("\nSTRAIGHT, LEFT or RIGHT: ")
#strength = int(input("\nStrength (0-5): "))
#drive_leader(speed,direction,strength)
#time.sleep(1)
#for i in range(10):
 #   if direction == 'STRAIGHT':
        
 #   time.sleep(0.5)
    
#stop()




#testing drive() and const_enc()
for j in range(3):
   i=41
#while i < 101: 
   speed = 100
   direction = 'RIGHT'
   
   speed = drive(speed, direction, 10)
   L = enc_read(0)-offset[0]
   R = enc_read(1)-offset[1]
   print(L,R)
   
   i+=const_enc(speed,direction,i)


stop()


        
'''
