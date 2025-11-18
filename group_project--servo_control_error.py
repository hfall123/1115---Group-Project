#function to collect and store servo control errors at 10 degree intervals (Amanda)

def servo_control_error(cleaned_file): 
    #if the first element in the list is a G1, the second is the shoulder value (x degrees) and the third is the elbow value (x degrees)

    #if the firts element is M5, then move the pen up (wrist servo: 30 degrees)

    #if the first elemetn is M3, then move the pen down (wrist servo: 0 degrees)

    #record the results of the test in a separate file so that we can refer back to it later for error values
  
    return #returns error value chart to refer back to later on for error values
