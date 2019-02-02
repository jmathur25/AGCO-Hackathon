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

# splits the data intro a train dataframe and validate dataframe randomly
def split_train_validate(df, frac):
    df_train = df.sample(frac=frac)
    df_validate = df.loc[~df.index.isin(df_train.index)]
    return df_train, df_validate

# replaces the missing vals in the dataframe with the median
# also creates a new column with T/F values on whether that value is null, so RF can use it!
def replace_missing_vals(df, col, name, na_dict):
    # checks if there are nulls in the column or if the
    if pd.isnull(col).sum() or (name in na_dict):
        # creates a column with T/F values per row on whether that row is null
        df[name + '_na'] = pd.isnull(col)
        # na_dict keeps track of the medians found for columns
        if name in na_dict:
            filler = na_dict[name]
        else:
            filler = col.median()
        # here is where the replacement happens
        df[name] = col.fillna(filler)
        na_dict[name] = filler
    return na_dict

# splits the dataframe into a dataframe with just params and the target y as its own dataframe
# also drops any columns not needed (put as list in skips)
def split_df_y(df, y_col_name, skips=None, na_dict=None):
    df = df.copy()
    y = df[y_col_name].values
    if skips is None:
        skips = y_col_name
    else:
        skips.append(y_col_name)
    df.drop(skips, axis=1, inplace=True)
    if na_dict is None:
        na_dict = {}
    # not sure what name, column are but it's what he uses lol
    # not sure what df.items() returns either
    for name, column in df.items():
        na_dict = replace_missing_vals(df, column, name, na_dict)
    return df, y, na_dict

# the imports we need to run Random Forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_jobs = -1)

# splitting via the 80/20 rule
train_data, validate_data = split_train_validate(machine_data, 0.8)

# creates the split dataframes for the train and validate datasets
# the target_y_name is the name of the column we want to predict
# the skip_fields is other columns we want to drop
target_y_name = "YIELD"
skip_fields = ["PROCESS_ID", "DATE", "YIELD_TOTAL", "YIELD_AVERAGE"]
# na_dict keeps track of the columns which had nulls and their medians
# need to use this in validate_data to make sure medians used across both dataframes
train_data_params, train_yield, na_dict = split_df_y(train_data, target_y_name, skips=skip_fields)

# the extra na_dict param makes sure na_dict medians from train used in validate!
validate_data_params, validate_yield, _ = split_df_y(validate_data, target_y_name, skips=skip_fields, na_dict=na_dict)

print("This is the train parameter-only data")
print(train_data_params.head())

print("This is the train output-only data")
print(train_yield.head())

print("This is the validate parameter-only data")
print(validate_data_params.head())

print("This is the validate output-only data")
print(validate_yield.head())

# the model is fit on the train data
rf.fit(train_data_params, train_yield)
# the model is evaluated using its weights on the validate)
print("Model score using defaults")
rf.score(validate_data_params, validate_yield)


# to use some more features of Random Forest
rf = RandomForestRegressor(n_estimators=40, min_samples_leaf=3, max_features=0.5, n_jobs=-1)
rf.fit(train_data_params, train_yield)
print("Model score using custom input parameters")
rf.score(validate_data_params, validate_yield)

# to see how estimators do at a tree level, search
# preds = np.stack([t.predict(X_valid) for t in rf.estimators_])
# on the RF doc and work from there. X_valid will have to be replaced with actual validation data variable name

# this makes a table to see how important various features of rf are!!
# def rf_feature_importance(rf, df):
#     return pd.DataFrame({'cols':df.columns, 'importance':rf.feature_importances_}).sort_values('importance', ascending=False)

# features = rf_feature_importance(rf, train_data_params)
# to see the 10 most important features
# print(features[:10])
#
# def plot_features(features):
#     return features.plot('cols', 'importance', 'barh', figsize=(12,7), legend=False)
# plot_features(features)

# add this to make sure importance meets some threshold
# THRESHOLD = 0.005
# to_keep = features[features.imp>THRESHOLD].cols
# len(to_keep)
# fixes params to just be the ones you want
# df_keep = machine_data[to_keep].copy()


