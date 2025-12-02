#give an option to addd a degree, just for testing so no input error cases
#this test code willl be replaced and deleted later
degree = int(input("test number: "))

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

#print for testing
print(degree)
print(translate_degrees(degree))

#results:
#the max and min were wihtin the PWM value range (0 - 65505)
#test: passed


