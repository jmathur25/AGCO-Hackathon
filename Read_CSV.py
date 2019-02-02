import pandas as pd

filename = "CAN_Test_DATA.csv"

machine_data = pd.read_csv(filename, encoding='mac_roman')
print(machine_data.head())
