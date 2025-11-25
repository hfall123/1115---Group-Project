from machine import ADC, Pin
import time

# =========================
#   SETTINGS
# =========================
SMOOTH_LEN = 6        # number of samples for smoothing
STEP_SIZE = 1         # servo movement per step
STEP_DELAY = 5        # ms delay between servo steps

# =========================
#   SIMPLE SERVO CLASS
# =========================
class Servo:
    def __init__(self, pin):
        # import lazy to avoid errors if library differs
        from machine import PWM
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)
        self.angle = 90

    def write(self, angle):
        # clamp for safety
        angle = max(0, min(180, angle))
        self.angle = angle
        duty = int((angle / 180 * 2000) + 500)
        self.pwm.duty_u16(int(duty * 65))  # adjust scaling as needed

# =========================
#   SMOOTHER CLASS
# =========================
class Smoother:
    def __init__(self, length=5):
        self.n = length
        self.values = []

    def add(self, v):
        self.values.append(v)
        if len(self.values) > self.n:
            self.values.pop(0)
        return sum(self.values) / len(self.values)


# =========================
#   SMOOTH SERVO MOVEMENT
# =========================
def move_servo_smooth(servo, target_angle):
    current = servo.angle
    target = int(target_angle)

    if current < target:
        rng = range(current, target + 1, STEP_SIZE)
    else:
        rng = range(current, target - 1, -STEP_SIZE)

    for a in rng:
        servo.write(a)
        time.sleep_ms(STEP_DELAY)


# =========================
#   SETUP
# =========================
pot_x = ADC(26)
pot_y = ADC(27)

s_x = Smoother(SMOOTH_LEN)
s_y = Smoother(SMOOTH_LEN)

shoulder = Servo(0)   # your pin numbers here
elbow    = Servo(1)   # your pin numbers here


# =========================
#   MAP FUNCTION
# =========================
def map_value(v, in_min, in_max, out_min, out_max):
    return (v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


# =========================
#   MAIN LOOP
# =========================
while True:
    # Read raw ADCs
    raw_x = pot_x.read_u16()
    raw_y = pot_y.read_u16()

    # Smooth them
    smooth_x = s_x.add(raw_x)
    smooth_y = s_y.add(raw_y)

    # Convert ADC → servo angle
    ang_x = map_value(smooth_x, 0, 65535, 0, 180)
    ang_y = map_value(smooth_y, 0, 65535, 0, 180)

    # Move servos smoothly
    move_servo_smooth(shoulder, ang_x)
    move_servo_smooth(elbow, ang_y)

    time.sleep_ms(5)
