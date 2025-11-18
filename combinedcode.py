#write the skeleton code for the functions here,
#also choose which functions you would like to work on for the project (put your name above it on this file and the doc)

#function to read PWM singals from the knobs and send that info to the servo




#function to check accuracy of the servo
def error_value(expected_degree, actual_degree):
    #checks the angle value that the servo thinks it is at

    #checks the actual angle value from the encoder

    #subtracts the actual from the expected value to get the difference (error value)

    return #this will return the error value


#function to translate degree values to PWM values
def translate(degree):
    #ensure that the angle is one that is within the range of the servo (0-180)
    #if it isnt, ensure it does not try to go further than this limit (if it tries to go below 0, set it to 0... etc)

    #get the pulse width

    #get the duty cycle as a decimal value

    #multiply by 65535 to get a PWM value between 65535 and 0 

    return #returns translated PWM value


#function to move the servos to a specific location using inverse kinematics
def inverse_kinematics(wrist_x, wrist_y, shoulder_x, shoulder_y):
    #a try except to ensure that the values given are valid
    #equations to find the angle that the shoulder and arm servos should be at

    #convert the result to degrees

    return #returns the final calculated angles for the shoulder and arm servos


#function to read and parse the file for error testing
def read_file():
    #retrieve error testing coordinates form a separate file (testing every 10 degrees)
    #read, strip and split the file
    #add a time buffer so that the servo has time to complete the tasks and doesnt get overwhelmend
    return #returns stripped and split file


#function to collect and store servo control errors at 10 degree intervals
def servo_control_error(cleaned_file):
    #if the first element in the list is a G1, the second is the shoulder value (x degrees) and the third is the elbow value (x degrees)

    #if the firts element is M5, then move the pen up (wrist servo: 30 degrees)

    #if the first elemetn is M3, then move the pen down (wrist servo: 0 degrees)

    #record the results of the test in a separate file so that we can refer back to it later for error values
    return #returns error value chart to refer back to later on for error values
