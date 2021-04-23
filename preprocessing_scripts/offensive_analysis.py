"""Script to pre-process the offensive data and perform data exploration"""

import matplotlib.pyplot as plt
import pandas as pd
import re
import collections

# create dictionary of text file names
text_files = {"train text": "data/offensive/offensive_train.txt",
              "validation text": "data/offensive/offensive_validation.txt",
              "test text": "data/offensive/offensive_test.txt"}

# create dictionary of label file names
label_files = {"train labels": "data/offensive/offensive_train_labels.txt",
               "validation labels": "data/offensive/offensive_validation_labels.txt",
               "test labels": "data/offensive/offensive_test_labels.txt"}


# function to open and do basic cleanse of text data
def preprocess(set_file):
    emotion_data = []
    with open(text_files[set_file], 'r', encoding='utf-8') as f:
        for line in f:
            line = line.replace("@user", "")
            line = line.replace("#", "hashtag ")
            alphanumeric_filter = re.sub(r'[^A-Za-z0-9 ]+', '', line)
            new_line = "".join(alphanumeric_filter)
            emotion_data.append(new_line.replace("\n", ""))
    text_files[key] = emotion_data


# function to open label data
def open_labels(key):
    offensive_labels = []
    with open(label_files[key], 'r') as f:
        for line in f:
            offensive_labels.append(line.replace("\n", ""))
    label_files[key] = offensive_labels


# function to clean text one word at a time
def text_cleanse(string):
    # set values of items to be removed
    stop_words = ['the', 'a', 'and', 'is', 'be', 'will', "to", "i", "of", "you", "in", "my", "that", "it", "for", "on",
                  "me", "im", "with", "so", "this", "just"]
    # convert string to lower case
    string = string.lower()
    # remove unnecessary words
    string = ' '.join([word for word in string.split() if word not in stop_words])
    return string


# function to merge two lists to make tuple
def merge(list_1, list_2):
    merged_list = tuple(zip(list_1, list_2))
    return merged_list


# loop over text files to open
for key in text_files:
    preprocess(key)

# loop over label files to open
for key in label_files:
    open_labels(key)

# create dictionary to store dataframes
dataframes = {"train": None,
              "validation": None,
              "test": None}

clean_raw_data = {"train": None,
                  "validation": None,
                  "test": None}

# create iterable lists of dictionary keys
text_list = list(text_files)
labels_list = list(label_files)
dataframes_list = list(dataframes)

# loop over each data set to create dataframes and raw data for word frequency analysis
for i in range(3):
    dataset = merge(text_files[text_list[i]], label_files[labels_list[i]])
    X_train = [x[0] for x in dataset]
    y_train = [int(y[1]) for y in dataset]
    X_train = [text_cleanse(x) for x in X_train]
    clean_raw_data[dataframes_list[i]] = X_train
    dataframes[dataframes_list[i]] = pd.DataFrame({'Text': X_train, 'Target': y_train})

for i in dataframes.keys():
    file_name = 'data/offensive/{}_df.csv'.format(i)
    dataframes[i].to_csv(file_name, index=False)

print(dataframes["train"].head())
########################################################################################################################
"""The following section conducts some data exploration"""

# # exploratory analysis of Target values
# counts = pd.DataFrame(dataframes["train"]['Target'].value_counts())
# print(counts)
# counts.plot(kind="bar")
# plt.title("Offensive analysis classification distribution")
# plt.xlabel("Class")
# plt.ylabel("Count")
# plt.show()
#
# # word counts
# wordcount = {}
#
# for line in clean_raw_data["train"]:
#     for word in line.split():
#         if word not in wordcount:
#             wordcount[word] = 1
#         else:
#             wordcount[word] += 1
#
# n_print = int(input("How many most common words to print: "))
# print("The {} most common words are:".format(n_print))
# word_counter = collections.Counter(wordcount)
# for word, count in word_counter.most_common(n_print):
#     print(word, ":", count)
#
# # Create a data frame of the most common words
# # Draw a bar chart
# lst = word_counter.most_common(n_print)
# df = pd.DataFrame(lst, columns=['Word', 'Count'])
# df.plot.bar(x='Word', y='Count')
# plt.show()
