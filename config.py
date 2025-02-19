"""
Configuration file for flood risk analysis.

This file defines:
- LAND_USE_MAP: Mapping of land use pixel values to economic damage estimates.
- LAND_USE_PATH: File path for the land use raster, included w/ tool. Taken from CORINE Land Cover 2018 for Baden-Wurt.
- VELOCITY_THRESHOLD: Minimum velocity for flood risk consideration, any value under will be considered insignificant.
"""
LAND_USE_MAP = {
# First number is the pixel value, second number is the economic damage
    # Urban
    1: 50,   # Continuous urban fabric
    2: 40,   # Discontinuous urban fabric
    3: 30,   # Industrial or commercial units
    4: 30,   # Road and rail networks and associated land
    5: 25,   # Port areas
    6: 25,   # Airports

    # Extraction/Construction
    7: 20,   # Mineral extraction sites
    8: 20,   # Dump sites
    9: 15,   # Construction sites

    # Recreational
    10: 15,  # Green urban areas
    11: 15,  # Sport and leisure facilities

    # Agricultural
    12: 10,  # Non-irrigated arable land
    13: 15,  # Permanently irrigated land
    14: 15,  # Rice fields
    15: 20,  # Vineyards
    16: 20,  # Fruit trees and berry plantations
    17: 20,  # Olive groves
    18: 10,  # Pastures
    19: 12,  # Annual crops associated with permanent crops
    20: 12,  # Complex cultivation patterns
    21: 12,  # Land principally occupied by agriculture with significant areas of natural vegetation
    22: 12,  # Agro-forestry areas

    # Forest/Natural Vegetation
    23: 5,   # Broad-leaved forest
    24: 5,   # Coniferous forest
    25: 5,   # Mixed forest
    26: 8,   # Natural grasslands
    27: 8,   # Moors and heathland
    28: 8,   # Sclerophyllous vegetation
    29: 8,   # Transitional woodland-shrub

    # Bare/Unvegetated Areas
    30: 3,   # Beaches - dunes - sands
    31: 3,   # Bare rocks
    32: 3,   # Sparsely vegetated areas
    33: 1,   # Burnt areas
    34: 2,   # Glaciers and perpetual snow

    # Wetlands
    35: 15,  # Inland marshes
    36: 15,  # Peat bogs
    37: 15,  # Salt marshes
    38: 15,  # Salines
    39: 15,  # Intertidal flats

    # Water Bodies
    40: 10,  # Water courses
    41: 10,  # Water bodies
    42: 10,  # Coastal lagoons
    43: 10,  # Estuaries
    44: 10,  # Sea and ocean

    # No Data
    48: 0    # NODATA
}
LAND_USE_PATH = "data/U2018_CLC2018_V2020_20u1.tif"
VELOCITY_THRESHOLD = 1