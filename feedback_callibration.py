USE_VIRTUAL = True  #change this to false for real hardware 

def read_adc(samples=25):  #takes 25 then averages them to reduce "noise"
    if USE_VIRTUAL:
        #converts shoulder angle into ADC value
        base = int(shoulder_angle / 180 * 65535)  
        return sum([max(0, min(65535, base + random.randint(-10,10)+50)) for _ in range(samples)]) / samples
    else:  #code for hardware 
        return sum([adc_x.read_u16() for _ in range(samples)]) / samples  

def shoulder_write(angle):  
    global shoulder_angle  #enables the shoulder to update outside the function
    if USE_VIRTUAL:
        shoulder_angle = angle  #simulates moving the servo
        print(f"[Virtual] Shoulder moved to {angle}°")  #shows whats happening 
    else:  
        pass  # real servo code can be added here but for now it does nothing 

def move_capture(angle):
    shoulder_write(angle)   #move shoulder to target angle
    time.sleep(1)   #lets servo settle first
    return read_adc()  #returns what the actual reading was

def run_calibration():
    global shoulder_angle
    shoulder_angle = 90.0  # start angle for virtual servo
    data = {f"{a}deg": move_capture(a) for a in [0, 90, 180]}   #creates a dicionary for the values
    with open("calibration.json", "w") as f:  
        ujson.dump(data, f)   #converts to storage format so program remembers calibration between rus
    print("Calibration complete:", data)

run_calibration()
