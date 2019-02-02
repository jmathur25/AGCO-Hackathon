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
-figure out most important params from RF fit

OTHER ideas:
-SVM fitter
"""

def split_df_y(df, y_col_name, skips=None):
    df = df.copy()
    y = df[y_col_name].values
    if skips is None:
        skips = y_col_name
    else:
        skips.append(y_col_name)
    df.drop(skips, axis=1, inplace=True)
    return df, y



from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_jobs = -1)

target_y_name = "YIELD"
skip_fields = ["PROCESS_ID", "DATE", "YIELD_TOTAL", "YIELD_AVERAGE"]
machine_data_params, yield_data = split_df_y(machine_data, target_y_name, skips=skip_fields)
rf.fit(machine_data_params, yield_data)
rf.score(machine_data, yield_data)

