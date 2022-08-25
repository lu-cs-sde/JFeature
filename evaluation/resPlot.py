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
headers = ["Version", "Count", "Url", "ProjectName", "commit_id"]
# First we create a dataframe that reads all the csv files in the current folder
df = pd.DataFrame(columns=headers)
j = 0
for file in os.listdir(output_dir):
    if file.endswith(".csv"):
        df1 = pd.DataFrame(columns=headers)
        df1 = pd.read_csv(output_dir + "/"+file, names=headers)
        df1["commit_id"] = file.split("_")[1].split(".")[0]
        df = df.append(df1)


# We filter out all the rows that have Feature = "Lambda"
df = df[df["Count"] == "TryWithResources"]


# Count the row for each different "FileName"
df_count = df.groupby(["commit_id"]).count()

# drop last three columns
df_count = df_count.drop(df_count.columns[-3:], axis=1)

# print(df_count)
# Save the result to a csv file in the same directory as the input files
df_count.to_csv(path + "/TWR_count.csv")
