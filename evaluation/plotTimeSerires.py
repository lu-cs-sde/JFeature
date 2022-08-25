# This script creates a dataframe with the following columns:
# - Project: the name of the project
# - JAVA1: the number of times JAVA1 is used
#  ....
# - JAVA8: the number of times JAVA8 is used
# - Each JAVAX column has subcolumns: one subcolumn for each JAVAX feature

import pandas as pd
import numpy as np
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import os
from tabulate import tabulate

path = sys.argv[1]
output_dir = os.path.dirname(path)
# Read csv file called "lambda_count.csv"
df = pd.read_csv(path + "/lambda_count.csv")
# Add a row that is (5784 - "commit_id")
df["Commit"] = 5784 - df["commit_id"]
# Rename the column Version with "Occurrences"
df.rename(columns={"Version": "Occurrences"}, inplace=True)
print(df)
# Plot the result using seaborn
ax = sns.lineplot(x="Commit", y="Occurrences", data=df)
# Add grid
ax.grid(True)
# Add title
ax.set_title("Lambda Expressions usage in Mockito")
# Add x-axis label
ax.set_xlabel("Commit counter")
# Add y-axis label
ax.set_ylabel("Number of times Lambda is used")
# Draw red vertical line at x=5696
ax.axvline(x=5690, color="red")
# Add a note at x=5696 with the text "b3fc349" in the middle rotated by -90 degrees
ax.text(x=5690, y=400, s="6b818ba", rotation=-90)

# Save the plot to a file as svg
plt.savefig(path + "/lambda_count.pdf")
plt.show()
