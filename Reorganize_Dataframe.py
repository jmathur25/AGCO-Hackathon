import pandas as pd
import numpy as np

def generate_process_id_to_rows_dict(machine_data):
	process_id_to_rows_dict = {}
	machine_data_aslist = machine_data.values.tolist()

	for i in range(len(machine_data["process_id"])):
		current_id = machine_data["process_id"][i]
		if current_id in process_id_to_rows_dict.keys():
			process_id_to_rows_dict[current_id].append(machine_data_aslist[i])
		else:
			process_id_to_rows_dict[current_id]= [machine_data_aslist[i]]

	return process_id_to_rows_dict

def generate_param_name_to_param_value_map(row_list):
	param_name_to_param_value_map = {}

	# loops through items in all the rows for current process id
	for row in row_list:
		# gets the parameter corresponding to this row
		param_name = row[4]
		if param_name in param_name_to_param_value_map.keys():
			#adds param value to list
			param_name_to_param_value_map[param_name].append(row[6])
		else:
			param_name_to_param_value_map[param_name] = [row[6]]

	return param_name_to_param_value_map


def generate_processes(num_processes, param_name_to_param_value_map, reordered, reordered_row_count, param_list, process_id, date, throwout_row=None):
	# loops through all the processes we can create for this process id
	# each iteration for the loop will create a new row in reordered that is populated with the first free params it can find
	# each process will probably get more sparse with each iteration as the number of available rows for each param decreases
	for j in range(num_processes):
		skip_process = False

		current_process = {}
		current_process['PROCESS_ID'] = process_id
		current_process['DATE'] = date
		# goes through each parameter in hardcoded list of parameters
		for param in param_list:
			try:
				# pops a row off of the list of rows for current param, gets the can_value for that row (corresponds to 6th index)
				current_process[param] = param_name_to_param_value_map[param].pop()
				if param == throwout_row:
					if current_process[param] < 0.001:
						skip_process = True
						break
			except:
				# will go here if param_name_to_param_value_map[param] does not have any members left 
				if throwout_row:
					if param == throwout_row:
						skip_process = True
						break
				current_process[param] = None
		if skip_process:
			continue
		# adds new process onto reordered with unique row count
		reordered[reordered_row_count] = current_process
		reordered_row_count += 1
