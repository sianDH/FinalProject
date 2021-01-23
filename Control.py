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
pos = [0,front,0]                    # current position of GoPiGo wrt front of GoPiGo x,y,rot
L = 0                                # encoder val of left wheel
R = 0                                # encoder val of right wheel
last_update = 0                      # time at which last position update occured
r_offset = 11                        # offset to reduce speed_R by so the wheel rotate at the same rate


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



def const_enc(speed,direction):
    """
    Ensures that the wheels turn as expected by keeping difference between encoders constant while driving
    """
    #error variables
    global L, R, offset
    enc_diff = R-L                    #setpoint to make sure diff between enc is constant
    if direction == 'STRAIGHT':       #ensures diff is 0 for driving straight
        enc_diff = 0
    time.sleep(0.3)
    L = enc_read(0)-offset[0]         #update Left enc count
    R = enc_read(1)-offset[1]         #update Right enc count
    new_diff = R-L
    error = new_diff - enc_diff
    error_prev = 0

    #controller variables
    t_prev = -100                     #check time with high res timer
    Kp = 1                            #Proportional Gain
    Td = 0                            #Differential time
    Ti = 100000000000                 #Integral time
    I = 0                             #Integral summation
    

    #while the wheels are not at the same speed implement controller
    while abs(error) > 0:
        
        t = time.perf_counter()#check time with high res timer

        # PD control equation
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
        speed_R = speed - r_offset #adjust R speed with offset so that wheels move at same speed
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
    
    time1 = time.perf_counter()
    return(speed_L, speed_R, time1)

def position_update(speed_L, speed_R, time1, time2):
    global pos, last_update
    
    #if motors turning
    if speed_L > 51 or speed_R > 51: 
        L_ms = ((speed_L * 0.00079)-0.026)      #L speed in m per sec based on speed conversion graph of encoder data
        R_ms = (((speed_R+r_offset)*0.00079)-0.026)   #R speed in m per sec and compensate for offset to have wheels the same speed

        time2 = time.perf_counter()
        dt = time2 - time1

        x,y,theta = pos
        theta = theta + (wheel_C*(R_ms-L_ms)/(2*3.14*width))* dt
        x = x + (wheel_C*(L_ms+R_ms)*math.sin(angle_x(theta))/(4*3.14))* dt 
        y = y + (wheel_C*(L_ms+R_ms)*math.cos(angle_x(theta))/(4*3.14))* dt
        pos = [x,y,theta]
    last_update = time2
    print(pos,last_update)
    pass


#testing position update
start_timer = time.perf_counter()
enc_count = enc_read(1) - offset[1]
curr = time.perf_counter()
sub = float(curr-start_timer)


for j in range(65): 
   speed = 80
   direction = 'STRAIGHT'

   speed_L, speed_R, time1= drive(speed, direction, 40)
   print(speed_L, speed_R)
   time.sleep(0.1)
   time2 = time.perf_counter()
   position_update(speed_L, speed_R, time1, time2)
   
   
     
speed = drive(0,direction,0)#stop

'''
