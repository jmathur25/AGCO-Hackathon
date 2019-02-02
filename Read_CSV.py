import pandas as pd

filename = "CAN_Test_DATA.csv"

machine_data = pd.read_csv(filename, encoding='mac_roman')
print(machine_data.head())

print(machine_data.columns.values)
machine_data = machine_data.drop(columns='Unnamed: 0')
print(machine_data.head())
