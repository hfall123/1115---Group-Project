#import required libraries
from machine import Pin, ADC, PWM
import time
import math

potentiometer_l = ADC(Pin(27))
potentiometer_r = ADC(Pin(26))
sw5 = Pin(22, Pin.IN, Pin.PULL_DOWN)

#set up LED pin locations
led2 = Pin(17, Pin.OUT)
led1 = Pin(16, Pin.OUT)

shoulder = PWM(Pin(0))
elbow = PWM(Pin(1))
wrist = PWM(Pin(2))

elbow.freq(50)
shoulder.freq(50)
wrist.freq(50)

button_press = 0
L1 = 155
L2 = 155
shoulder_x = -50
shoulder_y = 140

#give an option to addd a degree, just for testing so no input error cases
#this test code willl be replaced and deleted later

# degree = int(input("test number: "))

#function to read PWM singals from the knobs and send that info to the servo
def translate_voltage(adc_object) -> int:

    #get the duty cycle as a number between 0-1
    duty_cycle = adc_object / 65535
    #get the pulse width
    pulse_width = duty_cycle * 20000
    #make that number a numebr between 0 and 180
    translated_degree = ((pulse_width - 500)/( 25000 - 5000)) * 180

    if translated_degree > 180:
        translated_degree = 180
    elif translated_degree < 0:
        translated_degree = 0

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

#function that gives you the proper location based off of information about the angles of the servo and arm lengths
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

    return servo_wrist_deg, servo_elbow_deg

while True:

    adc_p_l = potentiometer_l.read_u16()
    adc_p_r = potentiometer_r.read_u16()

    if sw5.value() == 1 and button_press%2 == 0:
        button_press = button_press + 1
        wrist.duty_u16(translate_degrees(0))
        time.sleep(0.2)

       
    elif sw5.value() == 1 and button_press%2 != 0:
        button_press = button_press + 1
        wrist.duty_u16(translate_degrees(30))
        time.sleep(0.2)


    shoulder_angle, elbow_angle = inverse_kinematics(0, 0)
    elbow.duty_u16(translate_degrees(elbow_angle))
    shoulder.duty_u16(translate_degrees(shoulder_angle))
    time.sleep(3)
