import pandas as pd
import csv

filename = "CAN_Test_DATA.csv"

with open(filename, encoding='mac_roman', newline='') as f:
	csv_reader = csv.reader(f)
	machine_data = list(csv_reader)

machine_data = pd.DataFrame(machine_data)

machine_data.columns = ['row', 'equipment_type', 'equipment_status', 'timestamp', 'can_id', 'can_name', 'can_unit', 'can_value']

print(machine_data.head(3))