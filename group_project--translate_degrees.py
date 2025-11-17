#function to translate degree values to PWM values
def translate_degrees(degree):
    #ensure that the angle is one that is within the range of the servo (0-180)
    #if it isnt, ensure it does not try to go further than this limit (if it tries to go below 0, set it to 0... etc)

    if degree > 180:
        degree = 180
    elif degree < 0:
        degree = 0

    #get the pulse width

    #get the duty cycle as a decimal value

    #multiply by 65535 to get a PWM value between 65535 and 0 

    return #returns translated PWM value
