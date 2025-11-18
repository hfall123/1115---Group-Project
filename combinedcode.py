#write the skeleton code for the functions here,
#also choose which functions you would like to work on for the project (put your name above it on this file and the doc) 

#import required libraries
from machine import Pin, ADC
import math

#set up LED pin locations
led2 = Pin(17, Pin.OUT)
led1 = Pin(16, Pin.OUT)

#give an option to addd a degree, just for testing so no input error cases
#this test code willl be replaced and deleted later
degree = int(input("test number: "))


#give insrucitons on reading potential error messages to the users
print("""if there is any errors in the accuracy of the servo, the red light will turn on.
      if there are no issues, you will see a green light displayed on the expansion board""")

#function to read PWM singals from the knobs and send that info to the servo
def translate_voltage(adc_object: ADC) -> int:
    """
    Reads the current voltage from an initialized potentiometer ADC object (0–65535)
    and converts it to an angle between 0° and 180°.
    """
    MAX_ADC_READING = 65535
    MAX_DEGREES = 180
    SCALE = MAX_DEGREES / MAX_ADC_READING

    try:
        raw_value = adc_object.read_u16()
        angle = int(raw_value * SCALE)
        return max(0, min(MAX_DEGREES, angle))

    except AttributeError:
        print("ERROR: Invalid object passed to translate_voltage. Check initialization.")
        return 90
    except Exception as e:
        print(f"FATAL READ ERROR: {e}")
        return 90


#function to check accuracy of the servo
def error_value():
    #checks the angle value that the servo thinks it is at

    expected_degree = int(input("expected: ")) #will include translate_voltge(voltage) for final product

    #checks the actual angle value from the encoder
    actual_degree = int(input("actual: ")) #will insert code which can read the value form the encoder for final product

    #subtracts the actual from the expected value to get the difference (error value)
    error = expected_degree - actual_degree

    #return the error value so that it can be communicated to the user if there is an issue
    return error

#if the error value is above a certain amount, notify the user using LEDs
if error_value() > 2 or error_value() < -2:
    led1.value(1)
    led2.value(0)
    #notify the user of the severety of the error in the terminal
    print("""there seems to be a problem with the servo, 
    the difference between the degree it shoudl be set at and the angle it is actually set as is """, error_value())
else:
    led1.value(0)
    led2.value(1)

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



# computes shoulder and elbow servo angles required to move pen to desired position
def inverse_kinematics(x, y, L1, L2):
    # distance from shoulder base to target point
    r = math.sqrt(x*x + y*y)

    # checks reachability / mechanical limits
    if r > (L1 + L2) or r < abs(L1 - L2):
        return None  # point is physically impossible to reach

    # elbow angle
    cos_elbow = (r*r - L1*L1 - L2*L2) / (2 * L1 * L2)
    theta_elbow = math.acos(cos_elbow)

    # shoulder angle
    k1 = L1 + L2 * math.cos(theta_elbow)
    k2 = L2 * math.sin(theta_elbow)
    theta_shoulder = math.atan2(y, x) - math.atan2(k2, k1)

    # converts to degrees
    theta_shoulder_deg = math.degrees(theta_shoulder)
    theta_elbow_deg    = math.degrees(theta_elbow)

    return theta_shoulder_deg, theta_elbow_deg


#function to read and parse the file for error testing
def read_file(): 
    #retrieve error testing coordinates form a separate file (testing every 10 degrees)
    
    filename = "commands.txt"
    parsed = []     #empty list to store the processed commands
    
    #read, strip and split the file

    try:
        with open(filename, "r") as f:   #opens file in read only mode, names it f  
            lines = f.readlines()    #reads file 
    except OSError:    #if there is an issue accessing he file
        print("File not found:", filename)
        return []   #stops fuction and returns an empty list

    #add a time buffer so that the servo has time to complete the tasks and doesn't get overwhelmed

    for line in lines:    #loops through every line
        line = line.strip()    #cleans up line

        tokens = line.split()
        cmd = tokens[0].upper()  #makes the command uppercase
        entry = {"cmd": cmd}   #stores command and values associated with it 

        if cmd == "G1":     #checks if cmd is a movement command
            if len(tokens) < 3:    #checks values 
                continue     #skips line if values missing
            try:    #saves angles as integers
                entry["shoulder"] = int(tokens[1])  
                entry["elbow"] = int(tokens[2])
            except ValueError:
                continue

        elif cmd not in ("M3", "M5"):
            continue

        parsed.append(entry)

    return parsed #returns stripped and split file


#function to collect and store servo control errors at 10 degree intervals (Amanda)

def servo_control_error(cleaned_file):
    errors = []  #empty list to store error results
    
    #if the first element in the list is a G1, the second is the shoulder value (x degrees) and the third is the elbow value (x degrees)

    for entry in cleaned_file:   #loops trhough items in dictionary
        cmd = entry["cmd"]  #reads cmd type from dictionary
        if cmd == "G1":   #checks if cmd is for shoulder and elbow
            
            #assigns target angles from command dictionary to variables
            shoulder = entry["shoulder"]   
            elbow = entry["elbow"]
            
            #calculates the difference between expected and actual angles
            
            error_shoulder = error_value(shoulder, shoulder)
            error_elbow = error_value(elbow, elbow)
            errors.append({"cmd": "G1", "shoulder_error": error_shoulder, "elbow_error": error_elbow})

        #if the firts element is M5, then move the pen up (wrist servo: 30 degrees)

        elif cmd == "M5":  #checks if cmd moves pen up
            errors.append({"cmd": "M5", "wrist": 30})
            
            #if the first element is M3, then move the pen down (wrist servo: 0 degrees)

        elif cmd == "M3":   #checks if cmd moves pen down
            errors.append({"cmd": "M3", "wrist": 0})   

            #record the results of the test in a separate file so that we can refer back to it later for error values
        
            return errors #returns error value chart to refer back to later on for error values

#print for testing
print(degree)
print(translate_degrees(degree))
    return #returns error value chart to refer back to later on for error values
