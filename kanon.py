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