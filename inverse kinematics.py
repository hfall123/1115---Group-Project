def inverse_kinematics(Cx, Cy, La, Lb, theta_S_offset=0, theta_E_offset=0):
    # angle AC
    angle_AC = math.atan2(Cx, Cy)
    
    # length AC
    AC = math.sqrt(Cy**2 + Cx**2)
    
    # angle BAC
    angle_BAC = math.acos((La**2 + (AC**2) - Lb**2) / (2 * La * AC))
    
    # angle ABC
    angle_ABC = math.acos((La**2 + AC**2 - Lb**2) / (2 * La * Lb))
    
    # theta_AB
    theta_AB = angle_AC - angle_BAC
    
    # shoulder and elbow angles (with offsets)
    theta_S = theta_S_offset + theta_AB
    theta_E = angle_ABC - theta_E_offset
    
    # convert to degrees for servo control
    return math.degrees(theta_S), math.degrees(theta_E)
