#function to read and parse the file for error testing (Amanda)

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

