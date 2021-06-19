"""
These constants are intended to be used throughout both the rcpchgrowth module
and the API for validation of input values and rejection of very high or low values
"""

# HEIGHT CONSTANTS
MINIMUM_LENGTH_CM = 30
MAXIMUM_HEIGHT_CM = 300
# The tallest person for whom there is irrefutable evidence is
# Robert Pershing Wadlow who was 2.72m (8 ft 11.1 in) tall at his death in 1940
# https://en.wikipedia.org/wiki/Robert_Wadlow

# WEIGHT CONSTANTS
MINIMUM_WEIGHT_KG = 0.2
MAXIMUM_WEIGHT_KG = 500
# The heaviest man according to google is Jon Brower Minnoch (US)
# who had suffered from obesity since childhood. In September 1976,
# he measured 185 cm (6 ft 1 in) tall and weighed 442 kg (974 lb; 69 st 9 lb)
# https://en.wikipedia.org/wiki/Jon_Brower_Minnoch

# OFC CONSTANTS
MINIMUM_OFC_CM = 5
MAXIMUM_OFC_CM = 100
# We couldn't find a good answer for the 'largest human head' that we could use
# Instead have presumed that 100 is a good maximum, given that pathological states
# causing very large head size (eg hydrocephalus) render the OFC meaningless for
# growth measurement and assessment purposes.

# BMI CONSTANTS
MINIMUM_BMI_KGM2 = 7.5
MAXIMUM_BMI_KGM2 = 105
# Again, John Brower Minnoch comes to our rescue here. HIs body mass index
# at the time of his death was 105 kg/m2. In terms of the lowest body mass index ever recorded
# there was nly limited web search information that suggested 7.5 kg.m2 as the lowest ever.

# GESTATION CONSTANTS
MINIMUM_GESTATION_WEEKS = 22
MINIMUM_GESTATION_WEEKS_ERROR = f'It is very unlikely that a gestational age of less than {MINIMUM_GESTATION_WEEKS} weeks is correct'
MAXIMUM_GESTATION_WEEKS = 44
MAXIMUM_GESTATION_WEEKS_ERROR = f'It is very unlikely that a gestational age of more than {MAXIMUM_GESTATION_WEEKS} weeks is correct'
