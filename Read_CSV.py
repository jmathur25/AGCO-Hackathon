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

# splits the dataframe into a dataframe with just params and the target y as its own dataframe
# also drops any columns not needed (put as list in skips)
def split_df_y(df, y_col_name, skips=None):
    df = df.copy()
    y = df[y_col_name].values
    if skips is None:
        skips = y_col_name
    else:
        skips.append(y_col_name)
    df.drop(skips, axis=1, inplace=True)
    return df, y

# splits the data intro a train dataframe and validate dataframe randomly
def split_train_validate(df, frac):
    df_train = df.sample(frac=frac)
    df_validate = df.loc[~df.index.isin(df_train.index)]
    return df_train, df_validate

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
train_data_params, train_yield = split_df_y(train_data, target_y_name, skips=skip_fields)
validate_data_params, validate_yield = split_df_y(validate_data, target_y_name, skips=skip_fields)

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
def rf_feature_importance(rf, df):
    return pd.DataFrame({'cols':df.columns, 'imp':rf.feature_importances_}).sort_values('imp', ascending=False)

features = rf_feature_importance(rf, train_data_params)
# to see the 20 most important features
print(features[:20])

