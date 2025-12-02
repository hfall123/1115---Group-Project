#changed to translate position
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
