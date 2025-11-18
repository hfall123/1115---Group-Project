import math

# computes shoulder and elbow servo angles required to move pen to desired position
def inverse_kinematics(x, y, L1, L2):
    # distance from shoulder base to target point
    r = math.sqrt(x*x + y*y)

    # checks reachability / mechanical limits
    if r > (L1 + L2) or r < abs(L1 - L2):
        return None  # point is physically impossible to reach

    # elbow angle
    cos_elbow = (r*r - L1*L1 - L2*L2) / (2 * L1 * L2)
    theta_elbow = math.acos(cos_elbow)

    # shoulder angle
    k1 = L1 + L2 * math.cos(theta_elbow)
    k2 = L2 * math.sin(theta_elbow)
    theta_shoulder = math.atan2(y, x) - math.atan2(k2, k1)

    # converts to degrees
    theta_shoulder_deg = math.degrees(theta_shoulder)
    theta_elbow_deg    = math.degrees(theta_elbow)

    return theta_shoulder_deg, theta_elbow_deg
