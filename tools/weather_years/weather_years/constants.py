"""Physical constants, each derived from the source"""


HOURS_PER_YEAR = 8760
HOURS_PER_DAY = 24

SECONDS_PER_HOUR = 3600

PROFILE_TOTAL = 1 / SECONDS_PER_HOUR

J_TO_KWH = 2.77778e-7
CM2_TO_M2 = 1e-4

#: https://en.wikipedia.org/wiki/Properties_of_concrete
DENSITY_CONCRETE = 2400.0  # kg/m³
#: https://www.designingbuildings.co.uk/wiki/Specific_heat_capacity
SPECIFIC_HEAT_CAPACITY_CONCRETE = 880.0  # J/(kg·K)

# The reference house whose thermal mass sets the base heat capacity: a square
# 8x8x4 m house with a flat roof and 25 mm concrete envelope.
HOUSE_WIDTH = 8.0  # m
HOUSE_HEIGHT = 4.0 # m
WALL_THICKNESS = 0.025  # m

ROOF_AREA = HOUSE_WIDTH * HOUSE_WIDTH  # 64 m²
WALL_AREA = HOUSE_WIDTH * HOUSE_HEIGHT  # 32 m²
ENVELOPE_AREA = WALL_AREA * 4 + ROOF_AREA  # 192 m²
CONCRETE_MASS = ENVELOPE_AREA * WALL_THICKNESS * DENSITY_CONCRETE  # 11520 kg

#: Energy needed to raise the reference house by one kelvin, in kWh/K.
HEAT_CAPACITY_HOUSE = SPECIFIC_HEAT_CAPACITY_CONCRETE * J_TO_KWH * CONCRETE_MASS
