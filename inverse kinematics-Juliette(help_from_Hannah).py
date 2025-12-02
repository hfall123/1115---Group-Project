def inverse_kinematics(wrist_x, wrist_y):
    
    # Keeps arm inside drawing area
    if wrist_x > 20: 
        wrist_x = 20
    elif wrist_y < 20:
        wrist_y = 20
    
    # Distance from shoulder to target
    AC = math.sqrt(wrist_x**2 + wrist_y**2)

    # Check reachability
    if AC == 0:
        AC = 1

    # Angle from shoulder to target
    angle_AC = math.atan2(wrist_y, wrist_x)
    
    # Law of cosines for triangle at shoulder
    angle_BAC = math.acos((L1**2 + AC**2 - L2**2) / (2 * L1 * AC))

    # Shoulder angle
    theta_shoulder = angle_AC - angle_BAC

    # Law of cosines for elbow
    angle_elbow = math.acos((L1**2 + L2**2 - AC**2) / (2 * L1 * L2))
    
    theta_elbow = math.pi - angle_elbow  # elbow bends "down"

    # Apply servo offsets
    theta_shoulder += o_s_off
    theta_elbow += o_e_off

    # Convert to degrees
    shoulder_deg = math.degrees(theta_shoulder) - 80
    elbow_deg = math.degrees(theta_elbow)

    return shoulder_deg, elbow_deg

#add this to the while loop to handle errors and execute the code
shoulder, elbow = inverse_kinematics(shoulder_, elbow_)
    
if elbow > 180:
    elbow = 180
elif elbow < 0:
        elbow = 0




