import pandas as pd
import csv

filename = "CAN_Test_DATA.csv"

with open(filename) as f:
	csv_reader = csv.reader(f)
	machine_data = list(csv_reader)

machine_data = pd.DataFrame(machine_data)

print(machine_data.columns.tolist())