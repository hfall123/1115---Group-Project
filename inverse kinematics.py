#function that gives you the proper wrist location based off of information about the angles of the servo and arm lengths
def inverse_kinematics(wrist_x, wrist_y): 
    try:
        angle_AC = math.atan2(wrist_y,wrist_x)
        AC = math.sqrt(wrist_y **2 + wrist_x **2)
        angle_BAC = math.acos( (L1 ** 2 + (AC **2) - L2 **2)/ (2*L1*AC))
        angle_ABC = math.acos((L1**2 + AC**2 - L2**2)/(2*L1*L2))
        #find the angles each servo should be at
        theta_ab = angle_AC - angle_BAC
        servo_shoulder = o_s_off + theta_ab
        servo_elbow = angle_ABC - o_e_off

        servo_shoulder_deg = math.degrees(servo_shoulder)
        servo_elbow_deg = math.degrees(servo_elbow)

        #convert the resulting angles to degrees and find the correct angle for the servos
    except:
        #notfiy the user if there is an issue with completingt the calculations
        print("there has been an issue caluclating the proper anlge values using reverse kinematics")

    #return the angles that the servos should be at in order to reach the specified wrist coordinates
    return servo_shoulder_deg, servo_elbow_deg

