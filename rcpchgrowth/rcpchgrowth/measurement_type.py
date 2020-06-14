from .bmi_functions import bmi_from_height_weight, weight_for_bmi_height

class Measurement_Type:

    def __init__(self, measurement_type: str, height: float = None, weight: float = None, bmi: float = None, ofc: float = None, measurement_value: float = None):
        
        ## Measurement_Type class initalizes with a measurement type (height, weight, bmi or ofc)
        ## It can also accept a measurement_value if the measurement_type is specified
        ## and has two attribute measurement_type and observation_value

        self.measurement_type: str = measurement_type
        self.observation_value: float = None

        if measurement_type == 'bmi':
            if height is None and measurement_value is None:
                raise ValueError('Missing value for height. Cannot calculate a BMI.')
            elif weight is None and measurement_value is None:
                raise ValueError('Missing value for weight. Cannot calculate a BMI.')
            elif height is not None and height < 2:
                # most likely metres passed instead of cm.
                raise AssertionError('Height must be passed in cm, not metres')
            elif height is not None and height < 30.0:
                # a baby is unlikely to be < 30 cm long - probably a data entry error
                raise AssertionError(f'The height you have entered is very short. Are you sure you meant {30} cm?')
            elif height and weight:
                self.observation_value = bmi_from_height_weight(height, weight)
            elif measurement_value is not None:
                self.observation_value = measurement_value
            else:
                raise ValueError('Missing or incorrect measurement_type passed. Height in cm and weight in kg are required.')

        elif measurement_type == 'height':
            if height is None and measurement_value is None:
                raise ValueError('Missing value for height. Please pass a height in cm.')
            elif height is not None and height < 2:
                # most likely metres passed instead of cm.
                raise AssertionError('Height must be passed in cm, not metres')
            elif height is not None and height < 30.0:
                # a baby is unlikely to be < 30 cm long - probably a data entry error
                raise AssertionError(f'The height you have entered is very short. Are you sure you meant {30} cm?')
            elif height:
                self.observation_value = height
            elif measurement_value is not None:
                self.observation_value = measurement_value
            else:
                raise ValueError('Missing or incorrect measurement_type passed. Height in cm is required.')

        elif measurement_type == 'weight':
            if weight is None and measurement_value is None:
                raise ValueError('Missing value for weight. Please pass a weight in kilograms.')
            elif weight is not None and weight < 0.20:
                # 200g is very small. Like this is an error
                raise AssertionError('Error. Please pass and accurate weight in kilograms')
            elif weight is not None and weight > 500.0:
                # it is likely the weight is passed in grams, not kg. The heaviest man according to google is 
                # Jon Brower Minnoch (US), who had suffered from obesity since childhood. In September 1976,
                # he measured 185 cm (6 ft 1 in) tall and weighed 442 kg (974 lb; 69 st 9 lb)
                raise AssertionError(f"Height must be passed in kg.")
            elif weight:
                self.observation_value = weight
            elif measurement_value is not None:
                self.observation_value = measurement_value
            else:
                raise ValueError('Missing or incorrect measurement_type passed. Weight in kg is required.')

        elif measurement_type == 'ofc':
            if ofc is None and measurement_value is None:
                raise ValueError('No value for head circumference. Please pass a head circumference in cm.')
            elif ofc is not None and ofc < 5.0:
                # A head circumference less than 5 cm is likely to be an error
                raise AssertionError('Error. Please pass an accurate height in cm.')
            elif ofc is not None and ofc > 150.0:
                # A head circumference > 150 cm is likely to be an error
                raise AssertionError('Error. Please pass an accurate height in cm.')
            elif ofc:
                self.observation_value = ofc
            elif measurement_value is not None:
                self.observation_value = measurement_value
            else:
                raise ValueError('Missing or incorrect measurement_type passed. Head circumference in cm is required.')