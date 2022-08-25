# Author Idriss Riouak
# Date: 2022-02-22
# Description: two arguments are read from the commandline:
#  - @arg1: the path to the csv file to read
#  - @arg2: project name. This is used to save the plots
# Output: plots with the name of the project are saved in the current folder.


from PyPDF2 import PdfFileMerger
from math import ceil
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
# from pywaffle import Waffle

path = sys.argv[1]
project = sys.argv[2]
output_dir = os.path.dirname(path)
common_prefix = output_dir+"/" + project


# creating a function that maps a version to a color:
# - cyan: JAVA1
# - magenta: JAVA2
# - orange: JAVA3
# - red: JAVA4
# - yellow: JAVA5
# - green: JAVA6
# - blue: JAVA7
# - purple: JAVA8
def get_color(version):
    if version == "JAVA1":
        return plt.cm.Paired(0)
    elif version == "JAVA2":
        return plt.cm.Paired(1)
    elif version == "JAVA3":
        return plt.cm.Paired(2)
    if version == "JAVA4":
        return plt.cm.Paired(3)
    elif version == "JAVA5":
        return plt.cm.Paired(4)
    elif version == "JAVA6":
        return plt.cm.Paired(5)
    elif version == "JAVA7":
        return plt.cm.Paired(6)
    elif version == "JAVA8":
        return plt.cm.Paired(7)
    else:
        return "black"


plt.rcParams["figure.autolayout"] = True

# creating a dataframe from the csv file. The headers are: Version, Feature, Url
headers = ["Version", "Feature", "Url", "ProjectName"]
df = pd.read_csv(path, names=headers)
# df = df.drop(columns=["Url"])


# Counting the number of times each version is used
versions = df.groupby(['Version'], as_index=True).count()
versions = versions.sort_values(by=['Version'], ascending=False)

# Getting the number of features
features = df.groupby("Feature").count()
# Ordering the features by number of uses
features = features.sort_values(by=['Version'], ascending=False)


fig, axs = plt.subplots(3, 2)
fig.suptitle(project)
fig.set_size_inches(15, 10)
axs[0, 0].bar(versions.index, versions["Feature"], color="blue")
axs[0, 0].set_title("Number of features per Java version")
axs[0, 1].bar(features.index, features["Version"], color="blue")
axs[0, 1].set_title("Number of times each feature is used")
# The  x labels to vertical
plt.xticks(rotation='vertical')
# Displaying the values on the bars
for i, v in enumerate(versions["Feature"]):
    axs[0, 0].text(i,  v, str(v), color="black", ha='center')
for i, v in enumerate(features["Version"]):
    axs[0, 1].text(i, v, str(v), color="black", ha='center')
# Increase figure size
# Coloring the bar in axs[0] with the color of the version
for i, v in enumerate(versions["Feature"]):
    axs[0, 0].bar(i, v, color=get_color(versions.index[i]))
for i, v in enumerate(features["Version"]):
    axs[0, 1].bar(i, v,  color=get_color(df.query("Feature == '" +
                                                  features.index[i] + "'").head(1)["Version"].item()))




# Saving the plot
# plt.savefig(common_prefix + "_features.png")


# Create a dataframe from the orignal one with the only difference that takes into consideration rows where the url contains the word "test"
df_test = df[df["Url"].str.contains("test")]
# Counting the number of times each version is used
versions_test = df_test.groupby(['Version'], as_index=True).count()
versions_test = versions_test.sort_values(by=['Version'], ascending=False)
# Getting the number of features
features_test = df_test.groupby("Feature").count()
# Ordering the features by number of uses
features_test = features_test.sort_values(by=['Version'], ascending=False)
# Plotting the results as above
# fig, axs = plt.subplots(2)
# fig.suptitle(project + " - Test")
axs[1, 0].bar(versions_test.index, versions_test["Feature"], color="blue")
axs[1, 0].set_title("Number of features per Java version - TESTS")
axs[1, 1].bar(features_test.index, features_test["Version"], color="blue")
axs[1, 1].set_title("Number of times each feature is used - TESTS")
# The  x labels to vertical
plt.xticks(rotation='vertical')
# Displaying the values on the bars
for i, v in enumerate(versions_test["Feature"]):
    axs[1, 0].text(i,  v, str(v), color="black", ha='center')
for i, v in enumerate(features_test["Version"]):
    axs[1, 1].text(i, v, str(v), color="black", ha='center')

# Coloring the bar in axs[0] with the color of the version
for i, v in enumerate(versions_test["Feature"]):
    axs[1, 0].bar(i, v, color=get_color(versions_test.index[i]))
for i, v in enumerate(features_test["Version"]):
    axs[1, 1].bar(i, v,  color=get_color(df_test.query("Feature == '" +
                                                       features_test.index[i] + "'").head(1)["Version"].item()))

# Create a dataframe from the orignal one with the only difference that takes into consideration rows where the url does not contain the word "test"
df_main = df[~df["Url"].str.contains("test")]
# Counting the number of times each version is used
versions_main = df_main.groupby(['Version'], as_index=True).count()
versions_main = versions_main.sort_values(by=['Version'], ascending=False)

# Getting the number of features
features_main = df_main.groupby("Feature").count()
# Ordering the features by number of uses
features_main = features_main.sort_values(by=['Version'], ascending=False)
# Plotting the results as above

axs[2, 0].bar(versions_main.index, versions_main["Feature"], color="blue")
axs[2, 0].set_title("Number of features per Java version - SRC")
axs[2, 1].bar(features_main.index, features_main["Version"], color="blue")
axs[2, 1].set_title("Number of times each feature is used - SRC")
# The  x labels to vertical
plt.xticks(rotation='vertical')
axs[0, 0].tick_params(axis='x', rotation=90)
axs[0, 1].tick_params(axis='x', rotation=90)
axs[1, 0].tick_params(axis='x', rotation=90)
axs[1, 1].tick_params(axis='x', rotation=90)
axs[2, 0].tick_params(axis='x', rotation=90)
axs[2, 1].tick_params(axis='x', rotation=90)

# Displaying the values on the bars
for i, v in enumerate(versions_main["Feature"]):
    axs[2, 0].text(i,  v, str(v), color="black", ha='center')
for i, v in enumerate(features_main["Version"]):
    axs[2, 1].text(i, v, str(v), color="black", ha='center')
# Coloring the bar in axs[2,0] with the color of the version
for i, v in enumerate(versions_main["Feature"]):
    axs[2, 0].bar(i, v, color=get_color(versions_main.index[i]))
for i, v in enumerate(features_main["Version"]):
    axs[2, 1].bar(i, v,  color=get_color(df_main.query("Feature == '" +
                                                       features_main.index[i] + "'").head(1)["Version"].item()))
# Saving the plot
plt.savefig(common_prefix + "_merged.pdf")


# Getting number of row in the dataframe
n_row = df.shape[0]


# Generate from version a dictionary scaled to 100. The default dictionary is the one with all the features to 0


dict_versions = {'JAVA1': 0, 'JAVA2': 0, 'JAVA3': 0,
                 'JAVA4': 0, 'JAVA5': 0, 'JAVA6': 0, 'JAVA7': 0, 'JAVA8': 0}
for i in versions.index:
    dict_versions[i] = (versions.loc[i, "Feature"] / n_row)*100

dict_versions_tests = {'JAVA1': 0, 'JAVA2': 0, 'JAVA3': 0,
                       'JAVA4': 0, 'JAVA5': 0, 'JAVA6': 0, 'JAVA7': 0, 'JAVA8': 0}
versions_test = df[df["Url"].str.contains("test")].groupby(
    ['Version'], as_index=True).count()
for i in versions_test.index:
    dict_versions_tests[i] = (versions_test.loc[i, "Feature"] / n_row)*100

dict_versions_main = {'JAVA1': 0, 'JAVA2': 0, 'JAVA3': 0,
                      'JAVA4': 0, 'JAVA5': 0, 'JAVA6': 0, 'JAVA7': 0, 'JAVA8': 0}
versions_main = df[~df["Url"].str.contains("test")].groupby(
    ['Version'], as_index=True).count()
for i in versions_main.index:
    dict_versions_main[i] = (versions_main.loc[i, "Feature"] / n_row)*100


# fig = plt.figure(
#     FigureClass=Waffle,
#     plots={
#         311: {
#             'values': dict_versions,
#             'labels': [f"{k} ({round(v,2)}%)" for k,
#                        v in dict_versions.items()],
#             'legend': {
#                 'loc': 'upper left',
#                 'bbox_to_anchor': (1.05, 1),
#                 'fontsize': 8
#             },
#             'title': {
#                 'label': 'Java versions used - Total',
#                 'loc': 'left'
#             },
#             'colors': [get_color(i) for i in dict_versions.keys()]
#         },
#         312: {
#             'values': dict_versions_tests,
#             'labels': [f"{k} ({round(v,2)}%)" for k,
#                        v in dict_versions_tests.items()],
#             'legend': {
#                 'loc': 'upper left',
#                 'bbox_to_anchor': (1.2, 1),
#                 'fontsize': 8
#             },
#             'title': {
#                 'label': 'Java versions used - Test',
#                 'loc': 'left'
#             },
#             'colors': [get_color(i) for i in dict_versions_tests.keys()]
#         },
#         313: {
#             'values': dict_versions_main,
#             'labels': [f"{k} ({round(v,2)}%)" for k,
#                        v in dict_versions.items()],
#             'legend': {
#                 'loc': 'upper left',
#                 'bbox_to_anchor': (1.3, 1),
#                 'fontsize': 8
#             },
#             'title': {
#                 'label': 'Java versions used - Src',
#                 'loc': 'left'
#             },
#             'colors': [get_color(i) for i in dict_versions_main.keys()]
#         },
#     },
#     rows=10,
#     # shared parameter among subplots
#     # colors=("#2196f3", "#ff5252", "#999999"),
#     figsize=(5, 10)  # figsize is a parameter of plt.figure
# )
# # Saving the plot
# plt.savefig(common_prefix + "_waffle.png")


# # pdfs = [common_prefix + "_features.png", common_prefix + "_waffle.png"]
# # merger = PdfFileMerger()
# # for pdf in pdfs:
# #     merger.append(pdf)
# # merger.write(common_prefix + "_merged.pdf")
# # merger.close()
