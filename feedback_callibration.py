USE_VIRTUAL = False  #checking if its for the virtual jig(true) or actual hardware (false)

# fix comments later on

def read_adc(samples=25):
    if USE_VIRTUAL:
        # For virtual testing only
        base = int(shoulder.angle / 180 * 65535)
        return sum([max(0, min(65535, base + random.randint(-10,10)+50)) for _ in range(samples)]) / samples
    else:
        # Real potentiometer reading
        return sum([pot.read_u16() for _ in range(samples)]) / samples  # 'pot' is your existing ADC object

def move_capture(angle):
    shoulder.write(angle) 
    time.sleep(1)          # wait for servo to settle
    return read_adc()

# the actual callibration code  

data = {f"{a}deg": move_capture(a) for a in [0, 90, 180]}

with open("calibration.json","w") as f:
    ujson.dump(data, f)

print("Calibration complete:", data)

