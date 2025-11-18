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

