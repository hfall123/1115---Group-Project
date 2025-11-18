import machine
from machine import ADC 

def translate_voltage(adc_object: ADC) -> int:
    """
    Reads the current voltage from an initialized potentiometer ADC object (0–65535)
    and converts it to an angle between 0° and 180°.
    """
    MAX_ADC_READING = 65535
    MAX_DEGREES = 180
    SCALE = MAX_DEGREES / MAX_ADC_READING

    try:
        raw_value = adc_object.read_u16()
        angle = int(raw_value * SCALE)
        return max(0, min(MAX_DEGREES, angle))

    except AttributeError:
        print("ERROR: Invalid object passed to translate_voltage. Check initialization.")
        return 90
    except Exception as e:
        print(f"FATAL READ ERROR: {e}")
        return 90
