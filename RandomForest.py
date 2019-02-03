from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from Read_CSV import run_all

"""
RANDOM FOREST IMPLEMENTATION
----------------------------
-assumes dataframe has each process id as a row and parameters as a column
-passed data should be called machine_data

NEED TO
-------
-handle nulls/empty vals for processes
-fit params to yield
-split data into testing and validation
-figure out most important params from RF fit

OTHER ideas
-----------
-SVM fitter
"""

# splits the data intro a train dataframe and validate dataframe randomly
def split_train_validate(df, frac):
    df_train = df.sample(frac=frac)
    df_validate = df.loc[~df.index.isin(df_train.index)]
    return df_train, df_validate

# replaces the missing vals in the dataframe with the median
# also creates a new column with T/F values on whether that value is null, so RF can use it!
def replace_missing_vals(df, col_df, col_name, na_dict, drop_list):
    # checks if there are nulls in the column or if the
    if pd.isnull(col_df).sum() or (col_name in na_dict):
        # creates a column with T/F values per row on whether that row is null
        df[col_name + '_na'] = pd.isnull(col_df)
        # na_dict keeps track of the medians found for columns
        if col_name in na_dict:
            filler = na_dict[col_name]
        else:
            filler = col_df.median()

        # here is where the replacement happens
        df[col_name] = col_df.fillna(filler)
        na_dict[col_name] = filler
        # thank you gods of pandas
        if pd.isnull(col_df).sum() == len(col_df):
            drop_list.append(col_name)
    return na_dict, drop_list

# splits the dataframe into a dataframe with just params and the target y as its own dataframe
# also drops any columns not needed (put as list in skips)
def split_df_y(df, y_col_name, skips=None, na_dict=None):
    df = df.copy()
    y = df[y_col_name]
    if skips is None:
        skips = y_col_name
    else:
        skips.append(y_col_name)
    df.drop(skips, axis=1, inplace=True)
    skips = []
    if na_dict is None:
        na_dict = {}
    # name is column name, column is column number
    for column_name, column_df in df.items():
        na_dict, _ = replace_missing_vals(df, column_df, column_name, na_dict, skips)
    df.drop(skips, axis=1, inplace=True)
    return df, y, na_dict


def fit_dfs(df1, df2):
    df1_cols = set(df1.columns.values)
    df2_cols = set(df2.columns.values)

    return_df_1 = df1.copy()
    return_df_2 = df2.copy()
    net_col_list = df1_cols.intersection(df2_cols)
    for col in df1_cols:
        # print(col)
        if col not in net_col_list:
            return_df_1.drop(col, axis=1, inplace=True)
    for col in df2_cols:
        if col not in net_col_list:
            return_df_2.drop(col, axis=1, inplace=True)

    return return_df_1, return_df_2

rf = RandomForestRegressor(n_jobs=-1)

# runs everything in Read_CSV
machine_data = run_all()
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
# print(len(train_data_params.columns.values))

# the extra na_dict param makes sure na_dict medians from train used in validate!
validate_data_params, validate_yield, _ = split_df_y(validate_data, target_y_name, skips=skip_fields, na_dict=na_dict)
# print(len(validate_data_params.columns.values))

# fits the columns of the dfs to each other so they should share exactly the same columns
train_data_params, validate_data_params = fit_dfs(train_data_params, validate_data_params)

# print("This is the train parameter-only data")
# print(train_data_params)
#
# print("This is the train output-only data")
# print(train_yield.head())
#
# print("This is the validate parameter-only data")
# print(validate_data_params)
#
# print("This is the validate output-only data")
# print(validate_yield.head())

# the model is fit on the train data
rf.fit(train_data_params, train_yield)
# the model is evaluated using its weights on the validate)
print("Model score using defaults")
print(rf.score(validate_data_params, validate_yield))


# to use some more features of Random Forest
# rf = RandomForestRegressor(n_estimators=40, min_samples_leaf=3, max_features=0.5, n_jobs=-1)
# rf.fit(train_data_params, train_yield)
# print("Model score using custom input parameters")
# print(rf.score(validate_data_params, validate_yield))

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
# to_keep = features[features.importance>THRESHOLD].cols
# len(to_keep)
# fixes params to just be the ones you want
# df_keep = machine_data[to_keep].copy()
