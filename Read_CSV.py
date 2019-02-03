def run_all():
    import pandas as pd
    import numpy as np

    from Reorganize_Dataframe import generate_day_to_rows_dict, make_process_events, day_to_dataframe

    filename = "CAN_Test_DATA.csv"

    # , nrows=10000
    machine_data = pd.read_csv(filename, encoding='mac_roman', nrows=10000)

    machine_data = machine_data.drop(columns='Unnamed: 0')
    # print(machine_data.head())

    PARAMETER_LIST = set(machine_data['can_name'])

    day_count = 0
    process_day_to_id = {}
    day_array = []
    day_to_num_processes = {}

    for i in range(len(machine_data["timestamp"])):
        timestamp = machine_data["timestamp"][i]
        date = timestamp[:10]
        if date in process_day_to_id:
            day = process_day_to_id[date]
            day_to_num_processes[day] = day_to_num_processes[day] + 1
        else:
            day = day_count
            process_day_to_id[date] = day
            day_count += 1
            day_to_num_processes[day] = 1
        day_array.append(day)


    machine_data['day'] = np.array(day_array)
    # print(set(machine_data['day']))
    # print(day_to_num_processes)
    # print(machine_data)

    day_to_rows_map = generate_day_to_rows_dict(machine_data)
    # print(day_to_rows_map[0])
    return make_process_events(day_to_rows_map)

    

print(run_all())