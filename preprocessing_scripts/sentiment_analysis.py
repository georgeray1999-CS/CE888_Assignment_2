# import matplotlib.pyplot as plt
# import pandas as pd
# import re
#
# sentiment_data = []
#
# with open('data/sentiment_train.txt', 'r', errors='ignore') as f:
#     for line in f:
#         line = line.replace("@user", "")
#         alphanumeric_filter = re.sub(r'[^A-Za-z0-9 ]+', '', line)
#         new_line = "".join(alphanumeric_filter)
#         sentiment_data.append(new_line.replace("\n", ""))
#
# # load in labels
# sentiment_labels = []
# with open('data/sentiment_train_labels.txt', 'r') as f:
#     for line in f:
#         sentiment_labels.append(line.replace("\n", ""))
#
#
# # function to clean text one word at a time
# def text_cleanse(string):
#     # set values of items to be removed
#     stop_words = ['the', 'a', 'and', 'is', 'be', 'will']
#     # convert string to lower case
#     string = string.lower()
#     # remove unnecessary words
#     string = ' '.join([word for word in string.split() if word not in stop_words])
#     return string
#
#
# def merge(list_1, list_2):
#     merged_list = tuple(zip(list_1, list_2))
#     return merged_list
#
#
# sentiment_dataset = merge(sentiment_data, sentiment_labels)
#
# X_train = [x[0] for x in sentiment_dataset]
# y_train = [int(y[1]) for y in sentiment_dataset]
# X_train = [text_cleanse(x) for x in X_train]
#
# df = pd.DataFrame({'Text': X_train, 'Target': y_train})
# # print(df)
#
# print(df.shape)
# counts = pd.DataFrame(df['Target'].value_counts())
# print(counts)
# counts.plot(kind="bar")
# plt.title("Sentiment analysis classification distribution")
# plt.xlabel("Class")
# plt.ylabel("Count")
# plt.show()
#

import matplotlib.pyplot as plt
import pandas as pd
import re
import collections

# create dictionary of text file names
text_files = {"train text": "data/sentiment/sentiment_train.txt",
              "validation text": "data/sentiment/sentiment_validation.txt",
              "test text": "data/sentiment/sentiment_test.txt"}

# create dictionary of label file names
label_files = {"train labels": "data/sentiment/sentiment_train_labels.txt",
               "validation labels": "data/sentiment/sentiment_validation_labels.txt",
               "test labels": "data/sentiment/sentiment_test_labels.txt"}


# function to open and do basic cleanse of text data
def open_cleanse(key):
    sentiment_data = []
    with open(text_files[key], 'r', errors='ignore') as f:
        for line in f:
            line = line.replace("@user", "")
            alphanumeric_filter = re.sub(r'[^A-Za-z0-9 ]+', '', line)
            new_line = "".join(alphanumeric_filter)
            sentiment_data.append(new_line.replace("\n", ""))
    text_files[key] = sentiment_data


# function to open label data
def open_labels(key):
    sentiment_labels = []
    with open(label_files[key], 'r') as f:
        for line in f:
            sentiment_labels.append(line.replace("\n", ""))
    label_files[key] = sentiment_labels


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
    open_cleanse(key)

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
    file_name = 'data/sentiment/{}_df.csv'.format(i)
    dataframes[i].to_csv(file_name, index=False)
########################################################################################################################

# # exploratory analysis of Target values
# counts = pd.DataFrame(dataframes["train"]['Target'].value_counts())
# print(counts)
# counts.plot(kind="bar")
# plt.title("Sentiment analysis classification distribution")
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

