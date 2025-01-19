import csv
import hashlib
from datetime import datetime

# Function that tokenizes one-way a dataset's EIs
def tokenize_dataset(dataset, EIs):
    tokenized_dataset = dataset[::]

    for i in range(len(tokenized_dataset)):
        for EI in EIs:
            original_value = tokenized_dataset[i][EI] 
            hash_function = hashlib.sha256()
            hash_function.update(original_value.encode())
            new_value = hash_function.hexdigest()

            tokenized_dataset[i][EI] = new_value

    return tokenized_dataset

# Hierarchy tree of education_tree
education_tree = {}

education_tree["-"] = "-"                                               # 1st place, index 0

# 1st level
education_tree["graduated"] = "-"                                       # 2nd place, index 1
education_tree["under graduated"] = "-"                                 # 3rd place, index 2
 
# 2nd level
education_tree["phd"] = "graduated"                                     # 4th place, index 3
education_tree["master degree"] = "graduated"                           # 5th place, index 4
education_tree["bachelor degree"] = "graduated"                         # 6th place, index 5
education_tree["second grade schools"] = "under graduated"              # 7th place, index 6

# Leaves
education_tree["high schools"] = "second grade schools"                 # 8th place, index 7
education_tree["middle schools"] = "second grade schools"               # 9th place, index 8
education_tree["elementary schools"] = "under graduated"                # 10th place, index 9

def generalize_function(value):
    if (value in education_tree):
        return education_tree[value]
    else:
        print(str(value) + " not found in education_tree.")
        exit()

