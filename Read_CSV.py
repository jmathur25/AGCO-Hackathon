import csv

filename = "CAN_Test_DATA.csv"

with open(filename) as f:
    csv_reader = csv.reader(f)
    combine_data = list(csv_reader)