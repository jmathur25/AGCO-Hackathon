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
	# list_of_common_params = set()
	first = True
	for key in day_to_rows_map.keys():
		if len(day_to_rows_map[key]) < 500:
			continue
		params_seen, break_row = find_first_valid_value_of_day(day_to_rows_map[key])
		day_dataframe = day_to_dataframe(params_seen, day_to_rows_map[key], break_row)
		if first:
			list_of_common_params = set(day_dataframe.columns.values)
		else:
			list_of_common_params = list_of_common_params.intersection(set(day_dataframe.columns.values))
		print(day_dataframe)
		whole_dataset.append(day_dataframe, ignore_index=True)
	print(list_of_common_params)
	return whole_dataset
