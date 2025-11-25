#add these ones before the main loop

# For storing smoothed potentiometer values
smooth_x = None
smooth_y = None

# For tracking servo angles (used by smooth servo movement)
# Make sure your servo class stores servo.angle — if not, add that.
shoulder_current = 90    # starting position
elbow_current    = 90    # starting position

#acc helper functions to smootj the lines


# Smooth noisy potentiometer inputs
def smooth(prev, new, factor=0.3):
    if prev is None:
        return new
    return prev * (1 - factor) + new * factor

# Convert ADC value (0–65535) to servo angle (0–180)
def map_adc_to_angle(val):
    return (val / 65535) * 180

# Move servo gradually to target angle
def move_servo_smooth(servo, target, step=1, delay=5):
    global shoulder_current, elbow_current
    
    target = int(target)

    # determine which angle variable to update:
    if servo == shoulder:
        current = shoulder_current
    else:
        current = elbow_current

    # choose movement direction
    if current < target:
        rng = range(current, target, step)
    else:
        rng = range(current, target, -step)

    # actually move
    for a in rng:
        servo.write(a)
        time.sleep_ms(delay)

    # update tracking variable
    if servo == shoulder:
        shoulder_current = target
    else:
        elbow_current = target
