import wordcloud
import random

total_param_list = {'CROP_TYPE', 'AREA_TOTAL', 'FUEL_TOTAL', 'GRAIN_BIN_FULL', 'AUTOGUIDE_STATUS',
					  'THRESHING_ON', 'ENGINE_HOURS', 'FEEDER_LOAD_AVERAGE', 'HARVEST_HOURS', 'MOISTURE',
					  'HEADER_SPEED', 'CAPACITY_Average', 'GRAIN_LOSS_Rotor', 'SAT_SIGNAL', 'FEEDER_SPEED',
					  'ROTOR_SPEED', 'TEST_WEIGHT', 'GRAIN_QUALITY_SENSOR_AUTOMATION_STATUS', 'GSM_SIGNAL',
					  'MOISTURE_AVERAGE', 'CONCAVE_POSITION', 'HEADER_HEIGHT', 'CAPACITY',
					  'COVERAGE_RATE_INSTANTANEOUS', 'CHAFFER_POSITION', 'SCR_ACTUAL_DOSING_QUANTITY',
					  'HYDR_OIL_LEVEL_ALARM', 'UNLOAD_AUGER_STATUS', 'OUTSIDE_AIR_TEMP', 'MACHINE_PITCH',
					  'GRAIN_BIN_1_NEAR_FULL', 'FAN_SPEED', 'FUEL_AREA', 'BATTERY_VOLTAGE', 'YIELD_TOTAL',
					  'DISTANCE', 'GPS_HEADING', 'YIELD', 'FUEL_RATE', 'CONTROL_BALANCE_GOAL',
					  'FUEL_DELIVERY_PRESSURE', 'ENGINE_ON', 'TOTAL_TAILINGS_VOLUME_PERCENT', 'MOG_ACTUAL',
					  'BROKEN_GRAIN_ACTUAL', 'GRAIN_LOSS_Shoe', 'ENGINE_SPEED', 'GRAIN_BIN_1_NEAR_EMPTY',
					  'MACHINE_ROLL', 'TRANS_OIL_TEMP', 'ENGINE_OIL_PRESS', 'SIEVE_POSITION',
					  'ENGINE_COOLANT_TEMP', 'HYDR_OIL_TEMP', 'FUEL_LEVEL', 'COMBINE_SPEED_CONTROL_MODE',
					  'ENGINE_LOAD', 'YIELD_AVERAGE', 'SCR_TANK_LEVEL', 'GRAIN_BIN_1_LEVEL', 'VEHICLE_SPEED',
					  'TRANS_GEAR', 'DEF_TOTAL', 'BEATER_SPEED', 'UNLOADER_SWING_STATE'}

dict_to_map = {}
for param in total_param_list:
    dict_to_map[param] = 1

def random_color_func():
    schemas = [(0, 51, 97), (0, 98, 98), (134, 199, 204), (128, 128, 128), (0, 0, 0), (122, 122, 212)]
    color = schemas[random.randrange(0, 6)]
    return color[0] + random.randrange(-10, 11), color[1] + random.randrange(-10, 11), color[2] + random.randrange(-10, 11)

# rgb is calculated per word with color_func random func; currently biased to darker, bluer hues
words_wordcloud = wordcloud.WordCloud(background_color='white', prefer_horizontal=0.3, contour_width=3,
                                      contour_color='purple', relative_scaling=0.4, min_font_size=5,
                                      color_func=lambda *args, **kwargs: random_color_func())
image = words_wordcloud.generate_from_frequencies(frequencies=dict_to_map)
image.to_file("wordMap.PNG")
