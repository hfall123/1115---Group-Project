#test 1:

#import required libraries
from machine import Pin, ADC, PWM
import time
import math

#set the pin locations of the potentiometers, servos, LEDs and buttons
potentiometer_l = ADC(Pin(27))
potentiometer_r = ADC(Pin(26))
sw5 = Pin(22, Pin.IN, Pin.PULL_DOWN)
led2 = Pin(17, Pin.OUT)
led1 = Pin(16, Pin.OUT)
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

#function to read PWM singals from the knobs and send that info to the servo
def translate_voltage(adc_object) -> int:

    #get the duty cycle as a number between 0-1
    duty_cycle = adc_object / 65535
    #get the pulse width
    pulse_width = duty_cycle * 20000
    #make that number a numebr between 0 and 180
    translated_degree = ((pulse_width - 500)/( 25000 - 5000)) * 180

    #ensure that the translated angle is one that is within the range of the servo (0-180)
    #if it isnt, ensure it does not try to go further than this limit (if it tries to go below 0, set it to 0... etc)
    if translated_degree > 180:
        translated_degree = 180
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
    try:
        AC = math.sqrt( (shoulder_x - wrist_x) ** 2 + (shoulder_y - wrist_y) ** 2 )
        A_C = math.sqrt( (shoulder_x - wrist_x) ** 2 + wrist_y ** 2 )
        _BAC = math.acos( (L1 ** 2 + int(AC) ** 2 - L2 ** 2) / (2 * L1 * AC) )
        _ACB = math.asin( (L1 * math.sin(_BAC)) / (L2) )
        _YAC = math.acos( ((shoulder_y**2) + (AC ** 2) - (A_C**2)) / ( (2) * (shoulder_y) * (AC) ))
        #find the angles each servo should be at
        wrist_value = _BAC + _YAC
        elbow_value = _BAC + _ACB 

        #convert the resulting angles to degrees and find the correct angle for the servos
        servo_wrist_deg = math.degrees(wrist_value) - 75
        servo_elbow_deg = 150 - math.degrees(elbow_value)
    except:
        #notfiy the user if there is an issue with completingt the calculations
        print("there has been an issue caluclating the proper anlge values using reverse kinematics")

    #return the angles that the servos should be at in order to reach the specified wrist coordinates
    return servo_wrist_deg, servo_elbow_deg

#a loop to keep the program running continuously
while True:
    #get the ADC values from each potentiometer
    adc_p_l = potentiometer_l.read_u16()
    adc_p_r = potentiometer_r.read_u16()

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

    #test for inverse kinematics
    shoulder_angle, elbow_angle = inverse_kinematics(0, 0)
    #result: equatoin was wrong, correct equation will be implemented in later testing

    #uses input directly from the potentiometer to move each servo
    #this will be switched to the inverse kinnematics degrees once the equation is verrified
    elbow.duty_u16(translate_degrees(elbow_angle))
    shoulder.duty_u16(translate_degrees(shoulder_angle))

    #time buffer for the inverse kinematics testing
    time.sleep(3)
