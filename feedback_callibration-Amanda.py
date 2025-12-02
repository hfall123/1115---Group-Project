#calibration code to account for the differences in the jigs

def read_adc(samples=25):  #takes 25 then averages them to reduce "noise"
        return sum([adc_x.read_u16() for _ in range(samples)]) / samples  

def move_capture(angle):
    shoulder_write(angle)   #move shoulder to target angle
    time.sleep(1)   #lets servo settle first
    return read_adc()  #returns what the actual reading was

def run_calibration():

    points = [0, 90, 180]    
    data = {f"{point}deg": move_capture(point) for point in points}   #creates a dicionary for the values
    with open("calibration.json", "w") as f:  
        ujson.dump(data, f)   #converts to storage format so program remembers calibration between rus
    print("Calibration complete:", data)

run_calibration()

#compensates for the variations detected 

def adc_to_angle(adc_value, calibration):
    # Extracts calibration points from the json file 
    adc0 = calibration["0deg"]
    adc90 = calibration["90deg"]
    adc180 = calibration["180deg"]

    if adc_value <= adc90:
        # interpolate between 0° and 90°
        return (adc_value - adc0) * 90 / (adc90 - adc0)
    else:
        # interpolate between 90° and 180°
        return 90 + (adc_value - adc90) * 90 / (adc180 - adc90)
