#test 3
#final test on inverse kinematics using physical board needs to be completed before demonstration
#implememtnation of servo callibration function

#import required libraries
from machine import Pin, ADC, PWM
import time
import math

#set the pin locations of the potentiometers, servos, LEDs and buttons
potentiometer_l = ADC(Pin(27))
potentiometer_r = ADC(Pin(26))
sw5 = Pin(22, Pin.IN, Pin.PULL_DOWN)
led_ok = Pin(17, Pin.OUT)
led_error = Pin(16, Pin.OUT)
shoulder = PWM(Pin(0))
elbow = PWM(Pin(1))
wrist = PWM(Pin(2))

#set the frequencies for the servos
elbow.freq(50)
shoulder.freq(50)
wrist.freq(50)

#set initial button presses to 0
button_press = 0

#set constants for inverse kinematics
L1 = 155
L2 = 155
shoulder_x = -50
shoulder_y = 140
o_s_off = 10
o_e_off = 35

#set the initial state of the LEDs 
led_ok.value(1)
led_error.value(0)

#function to read PWM singals from the knobs and send that info to the servo
def translate_position(adc_object) -> int:

    #get the duty cycle as a number between 0-1
    duty_cycle = adc_object / 65535
    #get the pulse width
    pulse_width = duty_cycle * 20000
    #make that number a numebr between the max and minimum coordinates (0 - 200)
    translated_degree = ((pulse_width - 500)/( 25000 - 5000)) * 200

    #ensure that the translated angle is one that is within the boudries of the paper (0-200)
    #if it isnt, ensure it does not try to go further than this limit (if it tries to go below 0, set it to 0... etc)
    if translated_degree > 200:
        translated_degree = 200
    elif translated_degree < 0:
        translated_degree = 0

    #return the translated value in degrees
    return translated_degree
    
#function to translate degree values to PWM values
def translate_degrees(degree):
    #ensure that the angle is one that is within the range of the servo (0-180)
    #if it isnt, ensure it does not try to go further than this limit (if it tries to go below 0, set it to 0... etc)
    if degree > 180:
        degree = 180
    elif degree < 0:
        degree = 0

    #get the puse width
    pulse_width = 500 + (2500 - 500) * degree / 180
    #get the duty cycle as a number between 0-1
    duty_cycle = pulse_width / 20000
    #make that number a numebr between 0 and 65535
    PWM_value = int(duty_cycle * 65535)

    #return the translated PWM value
    return PWM_value

#function that gives you the proper wrist location based off of information about the angles of the servo and arm lengths
def inverse_kinematics(wrist_x, wrist_y):
    
    #define bourdries so that the user cannot draw outside of the bounries of the page
    if wrist_x > 20:
        wrist_x = 20
    elif wrist_y < 20:
        wrist_y = 20
    
    # Distance from shoulder to target
    AC = math.sqrt(wrist_x**2 + wrist_y**2)

    #ensure there are no math errors as a result of division by 0
    if AC == 0:
        AC = 1

    #Angle from shoulder to target
    angle_AC = math.atan2(wrist_y, wrist_x)
    #Law of cosines for triangle at shoulder
    angle_BAC = math.acos((L1**2 + AC**2 - L2**2) / (2 * L1 * AC))
    #Shoulder angle
    theta_shoulder = angle_AC - angle_BAC
    #Law of cosines for elbow
    angle_elbow = math.acos((L1**2 + L2**2 - AC**2) / (2 * L1 * L2))
    theta_elbow = math.pi - angle_elbow  # elbow bends "down"
    #Apply servo offsets
    theta_shoulder += o_s_off
    theta_elbow += o_e_off
    #Convert to degrees
    shoulder_deg = math.degrees(theta_shoulder) - 80
    elbow_deg = math.degrees(theta_elbow)

    return shoulder_deg, elbow_deg

#give user instrucitons
print("""
        This is a drawing board.
      
        To use this peice of technology, turn the knobs on the expansion board.
        The left knob will move the pen up and down and the right knob will move the pen left and right.
        To place the pen on the paper, hit the button on the middle of the expansion board labled sw5.

        Before you use this drawing tool, it is reomeneded that you run a callibration test to ensure clean lines. 
        To do this, press the button on the top right of the expansion board labled sw4.
      
        if there are any issues running the program, the red light will illuminate on the board.
        otherwise you will only see the green one.
      """)

#a loop to keep the program running continuously
while True:
    try:
        #get the ADC values from each potentiometer
        adc_p_l = potentiometer_l.read_u16()
        adc_p_r = potentiometer_r.read_u16()
    except:
        print("there had been an issue recieving data from the potentiometers")
        led_ok.value(0)
        led_error.value(1)

    try:
        #set the shoulder anlge values to the values obtained from inverse kinematics
        shoulder_angle, elbow_angle = inverse_kinematics(translate_position(adc_p_l), translate_position(adc_p_r))
    except:
        print("there had been an issue calculating proper angle values using inverse kinematics")
        led_ok.value(1)
        led_error.value(0)

    
    try:
        #give the properly translated angle values to the servos
        elbow.duty_u16(translate_degrees(elbow_angle - 2106))
        shoulder.duty_u16(translate_degrees( shoulder_angle - 406)) 

        #for testing
        print("e ", elbow_angle - 2106)
        print("s ", shoulder_angle - 406)
    except:
        print("there had been an issue sending data to the servos")
        led_ok.value(0)
        led_error.value(1)

    #if the button is presses an even ammount of times, move the servo down
    if sw5.value() == 1 and button_press%2 == 0:
        #add one to the button press counter to keep track of how many times the button has been pressed
        button_press = button_press + 1
        #this degree will place the pencil on the page so that the user can draw
        wrist.duty_u16(translate_degrees(0))
        #a buffer to debounce the button
        time.sleep(0.2)

    #if the button is pressed an odd amount of times, move the servo 30 degrees up
    elif sw5.value() == 1 and button_press%2 != 0:
        #add one to the button press counter to keep track of how many times the button has been pressed
        button_press = button_press + 1
        #this degree will lift the pencil off the page so that the user can move the pencil wihtout drawing
        wrist.duty_u16(translate_degrees(30))
        #a buffer to debounce the button
        time.sleep(0.2)
