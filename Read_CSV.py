import pandas as pd
import numpy as np

filename = "CAN_Test_DATA.csv"

machine_data = pd.read_csv(filename, encoding='mac_roman', nrows=10000)

machine_data = machine_data.drop(columns='Unnamed: 0')
print(machine_data.head())

process_id_count = 0
process_day_to_id = {}
process_id_array = []
for i in range(len(machine_data["timestamp"])):
	timestamp = machine_data["timestamp"][i]
	date = timestamp[:10]
	if date in process_day_to_id.:
		process_id = process_day_to_id[date]
	else:
		process_id = process_id_count
		process_day_to_id[date] = process_id
		process_id_count += 1
	process_id_array.append(process_id)


machine_data['process_id'] = np.array(process_id_array)
print(set(machine_data['process_id']))

"""
RANDOM FOREST IMPLEMENTATION
-assumes dataframe has each process id as a row and parameters as a column
NEED TO
-handle nulls/empty vals for processes
-fit params to yield
-split data into testing and validation
-figure out most important params
"""
