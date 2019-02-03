import pandas as pd
import numpy as np


def generate_day_to_rows_dict(machine_data):
	process_id_to_rows_dict = {}
	machine_data_aslist = machine_data.values.tolist()

	for i in range(len(machine_data["day"])):
		current_id = machine_data["day"][i]
		if current_id in process_id_to_rows_dict.keys():
			process_id_to_rows_dict[current_id].append(machine_data_aslist[i])
		else:
			process_id_to_rows_dict[current_id]= [machine_data_aslist[i]]

	return process_id_to_rows_dict


def find_first_valid_value_of_day(rows, num_parameters=63):
	params_seen = {}
	break_row = 0
	for i in range(len(rows)):
		if len(params_seen.keys()) == num_parameters:
			break_row = i
			break
		params_seen[rows[i][4]] = rows[i][6]
	return params_seen, break_row


def day_to_dataframe(params_seen, rows, break_row):
	events = pd.DataFrame()
	for param in params_seen:
		events[param] = params_seen[param]
	for i in range(break_row+1, len(rows)):
		params_seen[rows[i][4]] = rows[i][6]
		events = events.append(params_seen, ignore_index=True)
	return events


def make_process_events(day_to_rows_map):
	whole_dataset = pd.DataFrame()
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
	first = True
	for key in day_to_rows_map.keys():
		# to ignore days with minimal data
		if len(day_to_rows_map[key]) < 500:
			continue
		params_seen, break_row = find_first_valid_value_of_day(day_to_rows_map[key])
		day_dataframe = day_to_dataframe(params_seen, day_to_rows_map[key], break_row)
		# finds which columns are missing
		cols_to_add = total_param_list - set(day_dataframe.columns.values)
		for col in cols_to_add:
			day_dataframe[col] = None
		# print(day_dataframe)
		if first:
			whole_dataset = day_dataframe
			first = False
		else:
			whole_dataset.append(day_dataframe, sort=True, ignore_index=True)

	return whole_dataset
