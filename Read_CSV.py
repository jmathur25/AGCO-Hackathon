import pandas as pd
import numpy as np

from Reorganize_Dataframe import generate_process_id_to_rows_dict, generate_param_name_to_param_value_map, generate_processes

NUMBER_OF_PARAMETERS = 63

filename = "CAN_Test_DATA.csv"

machine_data = pd.read_csv(filename, encoding='mac_roman', nrows=10000)

machine_data = machine_data.drop(columns='Unnamed: 0')
# print(machine_data.head())

PARAMETER_LIST = set(machine_data['can_name'])

process_id_count = 0
process_day_to_id = {}
process_id_array = []
process_id_to_num_processes = {}

for i in range(len(machine_data["timestamp"])):
	timestamp = machine_data["timestamp"][i]
	date = timestamp[:10]
	if date in process_day_to_id:
		process_id = process_day_to_id[date]
		process_id_to_num_processes[process_id] = process_id_to_num_processes[process_id] + 1
	else:
		process_id = process_id_count
		process_day_to_id[date] = process_id
		process_id_count += 1
		process_id_to_num_processes[process_id] = 1
	process_id_array.append(process_id)


machine_data['process_id'] = np.array(process_id_array)
# print(set(machine_data['process_id']))
# print(process_id_to_num_processes)

process_id_to_rows_map = generate_process_id_to_rows_dict(machine_data)

reordered = {}
reordered_row_count = 0

#loop through process ids
for i in range(len(process_id_to_rows_map.keys())):
	current_date = process_id_to_rows_map[i][0][2]
	
	# gets all of the rows that correspond to the current process id (which is i)
	current_row_list = process_id_to_rows_map[i]

	# create a dictionary that maps the parameter name to parameter value
	param_name_to_param_value_map = generate_param_name_to_param_value_map(current_row_list)
	
	# maximum number of processes that we can get from current process id (maximum number of rows for one param)
	num_processes = int((max([len(param_name_to_param_value_map[key]) for key in param_name_to_param_value_map.keys()]) - min([len(param_name_to_param_value_map[key]) for key in param_name_to_param_value_map.keys()]))/2)
	
	generate_processes(num_processes, param_name_to_param_value_map, reordered, reordered_row_count, PARAMETER_LIST, i, current_date)

by_parameter = pd.DataFrame(reordered).transpose()

print(by_parameter)








