import pandas as pd
import numpy as np

NUMBER_OF_PARAMETERS = 63

filename = "CAN_Test_DATA.csv"
#, nrows=10000
machine_data = pd.read_csv(filename, encoding='mac_roman')

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

process_id_to_rows_map = {}
machine_data_aslist = machine_data.values.tolist()

for i in range(len(machine_data["process_id"])):
	current_id = machine_data["process_id"][i]
	if current_id in process_id_to_rows_map.keys():
		process_id_to_rows_map[current_id].append(machine_data_aslist[i])
	else:
		process_id_to_rows_map[current_id]= [machine_data_aslist[i]]

reordered = {}
reordered_row_count = 0

# print(process_id_to_rows_map)
valid_count = 0
invalid_count = 0

#loop through process ids
for i in range(len(process_id_to_rows_map.keys())):
	current_date = process_id_to_rows_map[i][0][2]
	
	# create a dictionary that maps the parameter name to each row containing information about that parameter
	param_name_to_param_value_map = {}
	
	# gets all of the rows that correspond to the current process id (which is i)
	current_row_list = process_id_to_rows_map[i]
	
	# loops through items in all the rows for current process id
	# item represents each row
	for item in current_row_list:
		# gets the parameter corresponding to this row
		param_name = item[4]
		if param_name in param_name_to_param_value_map.keys():
			#adds param value to list
			param_name_to_param_value_map[param_name].append(item[6])
		else:
			param_name_to_param_value_map[param_name] = [item[6]]
	
	# maximum number of processes that we can get from current process id (maximum number of rows for one param)
	num_processes = int((max([len(param_name_to_param_value_map[key]) for key in param_name_to_param_value_map.keys()]) - min([len(param_name_to_param_value_map[key]) for key in param_name_to_param_value_map.keys()]))/2)
	
	# loops through all the processes we can create for this process id
	# each iteration for the loop will create a new row in reordered that is populated with the first free params it can find
	# each process will probably get more sparse with each iteration as the number of available rows for each param decreases
	for j in range(num_processes):
		current_process = {}
		current_process['PROCESS_ID'] = i
		current_process['DATE'] = current_date
		# goes through each parameter in hardcoded list of parameters
		for param in PARAMETER_LIST:
			try:
				# pops a row off of the list of rows for current param, gets the can_value for that row (corresponds to 6th index)
				current_process[param] = param_name_to_param_value_map[param].pop()
				valid_count += 1
				# print(current_process[param])
			except:
				# will go here if param_name_to_param_value_map[param] does not have any members  left 
				current_process[param] = None
				# print('here')
				invalid_count += 1
		# adds new process onto reordered with unique row count
		reordered[reordered_row_count] = current_process
		reordered_row_count += 1

df = pd.DataFrame(reordered)

print(df.transpose())
print(df.transpose()['YIELD'])
print(valid_count)
print(invalid_count)

counter = 0
for i in range(len(df.transpose()['YIELD'])):
	if df.transpose()['YIELD'][i]:
		print(df.transpose()['YIELD'][i])
		counter += 1

print(counter)







