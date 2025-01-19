import csv
import hashlib
from datetime import datetime

# Read the dataset
dataset = []

with open("dataset.csv", "r") as f:
    for row in csv.DictReader(f):
        dataset.append(row)

'''
function that takes in input a dataset and a list of
EIs attributes

and create a new dataset where 
all of the EI are tokenized (one way)
'''

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


'''
function that takes in input a dataset and a list of
EIs attributes

and create a new dataset where 
all of the EI are tokenized (two way)
'''

def tokenize2_dataset(dataset, EIs):
    tokenized_dataset = dataset[::]
    mapping_values = {}

    for i in range(len(tokenized_dataset)):
        for EI in EIs:
            original_value = tokenized_dataset[i][EI] 
            hash_function = hashlib.sha256()
            hash_function.update(original_value.encode())
            new_value = hash_function.hexdigest()

            mapping_values[new_value] = original_value
            tokenized_dataset[i][EI] = new_value

    return tokenized_dataset, mapping_values


#print(dataset[0])
tokenized_dataset, mapping_values = tokenize2_dataset(dataset[:5], ["name"])
#print(tokenized_dataset[0])

#print(mapping_values)

#print("TOKENIZED", tokenized_dataset[0]["name"])
#print("UNTOKENIZED", mapping_values[tokenized_dataset[0]["name"]])


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

print(list(education_tree).index("elementary schools"))

def age_generalization(date):
    # Counts the number of dashes in input: if one then it's a range, if two then it's a date
    count_dashes = date.count("-")
    
    if count_dashes == 2:
        # Date case
        birthdate = datetime.strptime(date, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        decade_start = (age // 10) * 10
        decade_end = decade_start + 10
        return f"{decade_start}-{decade_end}"
    
    elif count_dashes == 1:
        # Range case
        start, end = map(int, date.split("-"))
        difference = end - start

        if difference == 10:
            # Decade case
            twenty_years_start = (start // 20) * 20
            twenty_years_end = twenty_years_start + 20
            return f"{twenty_years_start}-{twenty_years_end}"
        elif difference == 20:
            # Case twenty years
            return "-"



def generalize_function(value):
    return education_tree[value]

'''
print("GENERALIZE ELEMENTARY x0", "Elementary school")
print("GENERALIZE ELEMENTARY x1", generalize_function(education_tree_tree, "Elementary school"))
print("GENERALIZE ELEMENTARY x2", generalize_function(education_tree_tree, generalize_function(education_tree_tree, "Elementary school")))
print("GENERALIZE ELEMENTARY x3", generalize_function(education_tree_tree, generalize_function(education_tree_tree, generalize_function(education_tree_tree, "Elementary school"))))
'''

'''
ORIGINAL
2325654
1234565
1232456
8765414
7652665
4575423
3462352
2368652
2467763

GENERALIZED x1
232565x
123456x
123245x
876541x
765266x
457542x
346235x
236865x
246776x

GENERALIZED x6
2xxxxxx
1xxxxxx
1xxxxxx
8xxxxxx
7xxxxxx
4xxxxxx
3xxxxxx
2xxxxxx
2xxxxxx
'''
'''
def generalize_numbers(values, level):
    
    if level == 0:
        return [str(v) for v in values]
    
    values_new = []
    for v in values:
        v_new = str(v)
        v_new = v_new[:-level] + ("x" * level)
        values_new.append(v_new)

    return values_new
'''

def myGeneralizeNumbers(value):
    count_x = value.count("x")+1
    v_new = str(value)
    v_new = v_new[:-count_x] + ("x" * count_x)
    return v_new


numbers = [
    "2325654",
    "1234565",
    "1232456",
    "8765414",
    "7652665",
    "4575423",
    "3462352",
    "2368652",
    "2467763"
]


'''
print(generalize_numbers(numbers, 0))
print(generalize_numbers(numbers, 1))
print(generalize_numbers(numbers, 2))
print(generalize_numbers(numbers, 3))
print(generalize_numbers(n-mbers, 4))
print(generalize_numbers(numbers, 5))
'''