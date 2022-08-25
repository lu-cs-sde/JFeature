# This script creates a dataframe with the following columns:
# - Project: the name of the project
# - JAVA1: the number of times JAVA1 is used
#  ....
# - JAVA8: the number of times JAVA8 is used
# - Each JAVAX column has subcolumns: one subcolumn for each JAVAX feature

import pandas as pd
import numpy as np
import sys
import os
from tabulate import tabulate

path = sys.argv[1]
output_dir = os.path.dirname(path)
headers = ["Version", "Feature", "Url", "ProjectName"]
# First we create a dataframe that reads all the csv files in the current folder
df = pd.DataFrame(columns=headers)
for file in os.listdir(output_dir):
    if file.endswith(".csv"):
        df1 = pd.DataFrame(columns=headers)
        df1 = pd.read_csv(output_dir + "/"+file, names=headers)
        df = df.append(df1)

# Now we create the dataframe described above
df_final = pd.DataFrame(columns=[
                        "Project", "JAVA1", "JAVA2", "JAVA3", "JAVA4", "JAVA5", "JAVA6", "JAVA7", "JAVA8"])
for index, row in df.iterrows():
    if row["ProjectName"] not in df_final.index:
        df_final.loc[row["ProjectName"]] = [
            row["ProjectName"], 0, 0, 0, 0, 0, 0, 0, 0]
    df_final.loc[row["ProjectName"]][row["Version"]] += 1

# drop the first column
df_final = df_final.drop(df_final.columns[0], axis=1)


# From the dataframe df that has the following columns:
# - Version: which JavaX we are using
# - Feature: the name of the feature
# - Url: the url of the compilation unit
# - ProjectName: the name of the project
# We want to create a dataframe that counts how many time a feature is used in a project. The inforamtion are taken from the dataframe df.

# Let's first extract all the unique projects name
projects = df["ProjectName"].unique()

# Extracting all the unique features
features = df["Feature"].unique()
# Adding space between character for each features

# Comment the next line if you want to prettyprint the table horizzontally
features = ["\n".join(x) for x in features]

features = np.insert(features, 0, "project")

# Creating a dataframe that will contain the number of times a feature is used in a project
df_features = pd.DataFrame(columns=features)
# For each project we will create a row in the dataframe
for project in projects:
    # For each feature we will create a column in the dataframe
    for feature in features:
        # We will create a row in the dataframe
        if feature == "project":
            df_features.loc[project] = project
        else:
            df_features.loc[project][feature] = 0
    # For each project we will count how many times a feature is used
    for index, row in df.iterrows():
        if row["ProjectName"] == project:
            df_features.loc[project]["\n".join(row["Feature"])] += 1
            # Uncomment this line if you want to prettyprint the table horizzontally
            # df_features.loc[project][row["Feature"]] += 1

# drop the first column
df_features = df_features.drop(df_features.columns[0], axis=1)

print(tabulate(df_final, headers='keys', tablefmt='psql'))
print(tabulate(df_features, headers='keys', tablefmt='psql'))

print(tabulate(df_final, headers='keys', tablefmt='plain'))
print(tabulate(df_features, headers='keys', tablefmt='plain'))
