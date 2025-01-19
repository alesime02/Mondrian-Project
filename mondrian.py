from kanon import is_k_anon
import generalize as gen
import csv
import os

education_list = list(gen.education_tree)

# Dataset opening from .csv file
def read_csv_if_exists(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return list(csv.DictReader(f))
    else:
        print(f"File '{filename}' not found.")
        return []

# Exports the result in a .csv file
def write_to_csv(dataset, output_file):
    fieldnames = dataset[0].keys()
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)

# Given a dataset and a list of QIs, this function counts the number of equivalence class in it.
def count_equivalence_classes(dataset, QIs):
    equivalence_classes = set()
    for row in dataset:
        key = tuple(row[QI] for QI in QIs)
        equivalence_classes.add(key)
    return len(equivalence_classes)

# Classical median value computation
def median(sequence):
    sequence = list(sorted(sequence))
    return sequence[ len(sequence) // 2 ]

# Median value computation on the list of education level of a partition given in input.
def median_education(sequence):
    positions = []
    for row_education in sequence:
        positions.append(education_list.index(row_education))
    educations_sorted = [education_list[i] for i in sorted(positions)]
    return educations_sorted[len(educations_sorted) // 2]
# It converts the list in a list of numbers, every number represents the level of the
# education (the list is in generate.py), later the list get sorted and reconverted.

# Finds the attribute with the greatest number of unique values.
def find_best_attribute(partition, QIs):
    values = []
    maxDim = 0
    maxQI = ""
    for QI in QIs:
        values.append( len( set( row[QI] for row in partition)) )
        if(values[-1] > maxDim):
            maxDim = values[-1]
            maxQI = QI
    return maxQI

# Classical frequency set computation
def frequency_set(partition, QI):
    frequency_set = {}
    for row in partition:
        value = row[QI]
        if value in frequency_set:
            frequency_set[value] += 1
        else:
            frequency_set[value] = 1
    return frequency_set

# Unique function to compute median value
def find_median_in_fs(fs, maxQI):
    value_list = list(fs.keys())
    if(maxQI == "education"):
        return median_education(value_list)
    return median(value_list)

# Generalizes a dataset, in the algorithm it is used to generalize the union of LHS and RHS.
def summarize(dataset, QIs):
    for qi in QIs:
        if(qi == "birthday"):
            for row in dataset:
                row[qi] = row[qi].split("-")[0]
            # Dataset sorting
            dataset.sort(key=lambda x: x[qi])
            # Generalized range for the attribute
            min_value = dataset[0][qi]
            max_value = dataset[-1][qi]
            if(min_value != max_value):
                generalized_value = f"[{min_value} - {max_value}]"
                # Substitute the real value with the generalized one
                for row in dataset:
                    row[qi] = generalized_value
        elif(qi == "zip-code"):
            # Dataset sorting
            dataset.sort(key=lambda x: x[qi]) 
            # Generalized range for the attribute
            min_value = dataset[0][qi]
            max_value = dataset[-1][qi]
            if(min_value != max_value):
                generalized_value = f"[{min_value} - {max_value}]"
                # Substitute the real value with the generalized one
                for row in dataset:
                    row[qi] = generalized_value
        elif(qi == "education"):
            while(len(set(row[qi] for row in dataset)) != 1):
                max = -1
                for row in dataset:
                    if(education_list.index(row[qi]) > max):
                        max = education_list.index(row[qi])
                for row in dataset:
                    if(education_list.index(row[qi]) == max):
                        row[qi] = gen.generalize_function(row[qi])
        elif(qi == "gender"):
            for row in dataset:
                row[qi] = "Any"

    return dataset

# Makes the dataset k-anonymous by generalizing QIs.
def mondrianAnon(dataset, QIs, K):
    # Check if dataset in already K anonymous, if true returns
    if (is_k_anon(dataset, QIs, K)):
        return dataset
    
    # This part is written by following the paper
    # dim ← choose dimension()
    maxQI = find_best_attribute(dataset, QIs)
    # fs ← frequency set(partition, dim)
    fs = frequency_set(dataset, maxQI)
    # splitVal ← find median(fs)
    splitVal = find_median_in_fs(fs, maxQI)
    # lhs ← {t ∈ partition : t.dim ≤ splitVal}
    LHS = [row for row in dataset if row[maxQI] <= splitVal]
    # rhs ← {t ∈ partition : t.dim > splitVal}
    RHS = [row for row in dataset if row[maxQI] > splitVal]

    # If both parts are greater than K, is still possible to cut the partition
    if((len(LHS) >= K) and (len(RHS) >= K)):
        return mondrianAnon(LHS, QIs, K) + mondrianAnon(RHS, QIs, K)
    
    # return Anonymize(rhs) ∪ Anonymize(lhs)
    return summarize((LHS+RHS), QIs)



dataset = read_csv_if_exists("dataset-big.csv")
with open("dataset-big.csv", "r") as f:
    for row in csv.DictReader(f):
        dataset.append(row)



# Result computation and parameters' setting
k = 5
QIs = ["zip-code", "education", "birthday","gender"]
EIs = ["id", "name"]
tokenized_dataset = gen.tokenize_dataset(dataset, EIs)
result = mondrianAnon(tokenized_dataset, QIs, k)
if(is_k_anon(result, QIs, k)):
    print("The table is "+str(k)+"-anonymous")


# Quality results
num_equivalence_classes = count_equivalence_classes(result, QIs)
C_avg = (len(dataset) / num_equivalence_classes) / k
upperbound = ((2 * len(QIs) * (k-1)) + num_equivalence_classes)/k
print("Number of equivalence classes: " + str(num_equivalence_classes))
print("Normalized average equivalence class size metric (C_avg): " + str(C_avg))
print("Upperbound to respect: " + str(C_avg) + " <= " + str(upperbound))

# Writes the result in a .csv file
output_file = "dataset-anonimized.csv"
write_to_csv(result, output_file)

print(f"The resultant table is exported in: '{output_file}'")