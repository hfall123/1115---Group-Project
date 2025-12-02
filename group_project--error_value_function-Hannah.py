#this is mostly for testing to ensure it can use the proper values once i have acess to them 
#from the other functions, until then, i will be using my imput as test values for expected and actual values

#import required libraries
from machine import Pin

#set up LED pin locations
led2 = Pin(17, Pin.OUT)
led1 = Pin(16, Pin.OUT)

#give insrucitons on reading potential error messages to the users
print("""if there is any errors in the accuracy of the servo, the red light will turn on.
      if there are no issues, you will see a green light displayed on the expansion board""")

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


