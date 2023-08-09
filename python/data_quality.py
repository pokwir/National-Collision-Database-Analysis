# %%
import pandas as pd
import numpy as np

# %%
data_path = '/Users/patrickokwir/Desktop/Git_Projects/National-Collision-Database-Analysis/dataset/y_2017_en.xlsx'

# %%
df = pd.read_excel(data_path)
df.head()

# %%


# %% [markdown]
# Data Profiling Exploration

# %%
# describe the data set
df.describe()

# %%
# check data type for each column
df.dtypes

# %%
# print unique values in a column
for col in df.columns:
    print (col, df[col].unique())

# %%
# return rows where C_MNTH = U
df[df['C_MNTH'] == 'UU']

# %%
# check for incomplete data
df.isnull().any(axis=1).sum()

# %%
#check for default values (duplicate C_CASE)
df['C_CASE'].value_counts().sort_values().tail(60)

# %%
df[df['C_CASE'] == 2544489]

# %% [markdown]
# Todo:
# - Completeness
# - Validity
# - Uniqueness
# - Consistency
# - Timeliness
# 

# %% [markdown]
# 1. Completeness: Completeness measures the degree to which all expected records in a dataset
# are present. At a data element level, completeness is the degree to which all
# records have data populated when expected. At a record level, completeness is the
# degree to which all data elements have data populated when expected.
# - check for missing records
# - check for missing data elements. 

# %%
# decode data using data_dict dictionary
# for each column, use column name to look lookup key in data_dict and return the values in the dictionary, replace the values in the df column with the values in the dictionary
for col in df.columns:
    df[col] = df[col].map(data_dict[col])

# %%
df.head()

# %%
# check for null values
df.isnull().sum().sort_values(ascending=False)

# %%
import os
import pandas as pd

def replace_values_with_data_keys(df, folder_path):
    for column in df.columns:
        csv_filename = os.path.join(folder_path, f"{column}.csv")
        
        if os.path.exists(csv_filename):
            data_keys = pd.read_csv(csv_filename)
            key_to_value = dict(zip(data_keys['Code'], data_keys['Description']))
            df[column] = df[column].replace(key_to_value)
        else:
            print(f"CSV file for column '{column}' not found.")
            
    return df

# %%
folder = '/Users/patrickokwir/Desktop/Git_Projects/National-Collision-Database-Analysis/notebooks'

# %%
df = replace_values_with_data_keys(df, folder)

# %%
df.head()

# %%
# Replace 'U' with Unknown in df
df = df.replace('U', 'Unknown')

# %%
# return rows where values is not "Unknown"
def filter_rows_with_unknown(df):
    unknown_rows = df[df.apply(lambda row: (row == 'Unknown').all(), axis=1)]
    return unknown_rows

# %%
filter_rows_with_unknown(df)

# %% [markdown]
# 2. Check for validity
#  
# Validity measures the degree to which the values in a data element are valid.

# %%
# Year must be 2017
# Month must be 1-12
# Wday must be 1-7
# Hour must be 0-23
# C_SEV must be 1-2


# %%
# check for Year
df['C_YEAR'].unique()

# %%
df['C_MNTH'].unique()

# %%
df['C_WDAY'].unique()

# %%
df['C_HOUR'].unique()

# %%
df['C_SEV'].unique()

# %%
# return rows where C_MNTH, C_WDAY, C_HOUR is 'Unknown'
unknown_rows = df[(df['C_MNTH'] == 'Unknown') & (df['C_WDAY'] == 'Unknown') & (df['C_HOUR'] == 'UU')]

# %%
unknown_rows

# %% [markdown]
# 3. Test for Uniqueness 
# 
# Uniqueness measures the degree to which the records in a dataset are not
# duplicated.

# %%
# check for duplicates
df.duplicated().sum()

# %%
df = df.replace('UU', 'Unknown')

# %%
df.to_csv('collision_2017.csv', index=False)

# %%



