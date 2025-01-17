import csv


'''
Function that return true / false
is dataset is k-anonymous

k-anonymous means
for each set of attrs (QI attributes) exists 
at least k rows in dataset with that set of QIs
'''
def is_k_anon(dataset, attrs, k):

    groups = {} # dictionary
    '''
    create a dictionary [attrs] -> rows

    for each row in dataset:
        put row in dictionary[row[attrs]]

    result = all(len(group) >= k for group in dictionary)
    '''
    for row in dataset:
        key = []
        for attr in attrs:
            key.append(str(row[attr]))

        key = "-".join(key)
        if key not in groups:
            groups[key] = []

        groups[key].append(row)

    result = True
    for group in groups:
        if len(groups[group]) < k:
            result = False
            break

    return result




'''
Function that return true / false
is dataset is l-diverse

l-diverse means
for each set of attrs (QI attributes) exists 
at least l differnet sensite value 
in the group with the same set of QIs
'''
def is_l_diverse(dataset, qi_attrs, sd_attrs, l):

    groups = {} # dictionary
    '''
    create a dictionary [attrs] -> rows

    for each row in dataset:
        put row in dictionary[row[qi_attrs]]

    result = all(len(set(group[sd_attrs])) >= l for group in dictionary)
    '''
    for row in dataset:
        key = []
        for attr in qi_attrs:
            key.append(str(row[attr]))

        key = "-".join(key)
        if key not in groups:
            groups[key] = []

        groups[key].append(row)

    result = True
    for group in groups:
        '''
        for each sensitive data attributes
        we need to have at least l diverse values inside the group

        diseases = [hearth, hearth, back, back, head, hand, leg, leg, head]
        set(diseases) = [hearth, back, head, hand, leg]
        len(set(diseases))) = 5
        '''
        for sd_attr in sd_attrs:
            sd_attr_values = []
            # I will create a list of different sd_attr value inside the group
            for row in groups[group]:
                sd_attr_values.append( row[sd_attr] )
            
            if len(set(sd_attr_values)) < l:
                result = False
                break

    return result


# T-CLOSENESS
'''
Function that return true / false
is dataset is t-closeness

t-closeness means
for each set of attrs (QI attributes) 

the statical distribution of the sensitive data inside the group 
is (more or less) the same of the statistical distribuite in the whole population

is_t_closeness(dataset, ["education"], ["salary"], 0.10)

-> is the average salary for each group of education level 
the same of the average salary of all the entries in the dataset with an error margin
of 10%? 

'''
def is_t_closeness(dataset, qi_attrs, sd_attrs, t):
    '''
    PSEUDCODE:

    create a dictionary [attrs] -> rows

    for each row in dataset:
        put row in dictionary[row[qi_attrs]]

    for each group in the dictionary:
        avg1 = evaluate the average value of the sensitive data in the group
        avg2 = evaluate the average value of the sensitive data in the whole dataset

        the average value in the group exceed the t % compared
        to the whole dataset
        if ((avg1-avg2) / avg2) > t:
            result = False
            break
    '''
    pass


# AVERAGE GLOBAL SALARY = 415691.23110796

'''
PEOPLE WITH ELEMENTARY DEGREE, HAS A SALARY OF (72958.71185907777, 121912.56817561336)
'''

# Read the small dataset for examples
'''
small_dataset = []

with open("dataset-small.csv", "r") as f:
    for row in csv.DictReader(f):
        small_dataset.append(row)


print(small_dataset)
print("LENGTH OF DATASET", len(small_dataset))

print("IS DATASET 1-ANON", is_k_anon(small_dataset, ["education"], 1))
print("IS DATASET 2-ANON", is_k_anon(small_dataset, ["education", "salary"], 2))
print("IS DATASET 3-ANON", is_k_anon(small_dataset, ["education"], 3))

print("IS DATASET 1-DIVERSE", is_l_diverse(small_dataset, ["education"], ["gender"], 1))
print("IS DATASET 2-DIVERSE", is_l_diverse(small_dataset, ["education"], ["gender"], 2))
print("IS DATASET 3-DIVERSE", is_l_diverse(small_dataset, ["education"], ["gender"], 3))


is_k_anon(dataset, ["city"], 3)

-> for each value of city, there are at least 3 different 
row in dataset with that specific city

ID, city, ...
1, genova, ...
2, milano, ...
3, milano, ...
4, genova, ...
5, roma, ...
6, milano, ...
7, milano, ...
8, roma, ...
9, roma, ...
10, genova, ...

is_k_anon(dataset, ["city"], 3) -> true

ID, city, ...
1, genova, ...
2, milano, ...
3, milano, ...
4, genova, ...
5, roma, ...
6, milano, ...
7, milano, ...
8, roma, ...
9, roma, ...

is_k_anon(dataset, ["city"], 3) -> false

'''