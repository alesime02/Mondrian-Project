from kanon import is_k_anon
import generalize as gen
import csv
import statistics

sequence = [1, 2, 2, 3, 4, 4, 4, 5, 6, 7, 8, 9, 9, 9, 9, 10, 11, 12, 13]

'''
1, 2, 3     <- % 2 = 1    -> median = 2
1, 2, 3, 4  <- % 2 = 0    -> median = (2+3) / 2 = 2.5
'''

def median(sequence):
    sequence = list(sorted(sequence))
    return sequence[ len(sequence) // 2 ]

def median_education(sequence):
    positions = []
    education_list = list(gen.education_tree)
    for row_education in sequence:
        positions.append(education_list.index(row_education))
    print(positions)  # Print the original positions for reference

    educations_sorted = [education_list[i] for i in sorted(positions)]
    return educations_sorted[len(educations_sorted) // 2]

'''med = median(sequence)
print("Median of sequence =", med)

LHS = [ f"<= {med}" for x in sequence if x <= med]
RHS = [ f"> {med}" for x in sequence if x > med]

print("SEQ = ", sequence)
print("LHS = ", LHS)
print("RHS = ", RHS)


sequence2 = ["Genoa", "Rome", "Milan",  "Rome", "Milan", "Genoa", "Genoa", "Genoa", "Milan", "Milan", "Genoa", "Rome", "Pisa", "Pisa", "Pisa"]
medianCity = median2(sequence2)

print("MEDIAN CITY =", medianCity)
LHS = [ x for x in sequence2 if x <= medianCity]
RHS = [ x for x in sequence2 if x > medianCity]

LHS = [ "[" + "-".join(list(set(LHS))) + "]" for x in LHS]
RHS = [ "[" + "-".join(list(set(RHS))) + "]" for x in RHS]

print("SEQ = ", sequence2)
print("LHS = ", LHS)
print("RHS = ", RHS)'''

# Con "dim" ho l'attributo con più elementi

# Con "frequency_set(partition, dim)" mi devo far restituire
# il vettore delle frequenze relative all'attributo dim

# In splitVal devo farmi restituire la mediana del vettore delle frequenze

# In LHS devo mettere tutti gli elementi della partizione che hanno il valore 
# dell'attributo "dim" minori o uguali alla mediana

# In RHS metto tutti gli elementi maggiori alla mediana

def find_best_attribute(partition, QIs):
    values = []
    maxDim = 0
    maxQI = ""
    for QI in QIs:
        # This will create a set with all the distinct values
        # for the currenct quasi-identifier
        values.append( len( set( row[QI] for row in partition)) )
        if(values[-1] > maxDim):
            maxDim = values[-1]
            maxQI = QI
    return maxQI

def frequency_set(partition, QI):
    frequency_set = {}
    for row in partition:
        value = row[QI]
        if value in frequency_set:
            frequency_set[value] += 1
        else:
            frequency_set[value] = 1
    return frequency_set

def find_median_in_fs(fs):
    value_list = list(fs.keys())
    return median(value_list)

def summarize(dataset, QIs):
    for qi in QIs:
        if(qi == "birthday"):
            for row in dataset:
                row[qi] = row[qi].split("-")[0]
            # Dataset sorting
            dataset.sort(key=lambda x: x[qi])
            # Calcola l'intervallo generalizzato per la colonna
            min_value = dataset[0][qi]
            max_value = dataset[-1][qi]
            generalized_value = f"[{min_value} - {max_value}]"
            # Sostituisci il valore nella colonna con l'intervallo generalizzato
            for row in dataset:
                row[qi] = generalized_value
        if(qi == "zip-code"):
            # Dataset sorting
            dataset.sort(key=lambda x: x[qi]) 
            # Calcola l'intervallo generalizzato per la colonna
            min_value = dataset[0][qi]
            max_value = dataset[-1][qi]
            generalized_value = f"[{min_value} - {max_value}]"
            # Sostituisci il valore nella colonna con l'intervallo generalizzato
            for row in dataset:
                row[qi] = generalized_value
        if(qi == "education"):
            while(len(set(row[qi] for row in dataset)) != 1):
                for row in dataset:
                    row[qi] = gen.generalize_function(row[qi])

    return dataset

# Makes the dataset k-anonymous by
# generalizing QIs
def mondrianAnon(dataset, QIs, K):
    # Check if dataset in already K anonymous, if true stop
    if (is_k_anon(dataset, QIs, K)):
        return dataset
    
    # I have some quasi-identifier to generalize
    # dim ← choose dimension()
    maxQI = find_best_attribute(dataset, QIs)
    # fs ← frequency set(partition, dim)
    fs = frequency_set(dataset, maxQI)
    # splitVal ← find median(fs)
    splitVal = find_median_in_fs(fs)
    # lhs ← {t ∈ partition : t.dim ≤ splitVal}
    LHS = [row for row in dataset if row[maxQI] <= splitVal]
    # rhs ← {t ∈ partition : t.dim > splitVal}
    RHS = [row for row in dataset if row[maxQI] > splitVal]
    # return Anonymize(rhs) ∪ Anonymize(lhs)
    if((len(LHS) >= K) and (len(RHS) >= K)):
        return mondrianAnon(LHS, QIs, K) + mondrianAnon(RHS, QIs, K)
    return summarize((LHS+RHS), QIs)

small_dataset = []

with open("dataset-small.csv", "r") as f:
    for row in csv.DictReader(f):
        small_dataset.append(row)

#mondrianAnon(small_dataset, ["zip-code", "education"], 3)

# Scrive il risultato in un file CSV
def write_to_csv(dataset, output_file):
    # Determina i campi (colonne) del dataset dal primo elemento
    fieldnames = dataset[0].keys()

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Scrive l'intestazione
        writer.writerows(dataset)  # Scrive i dati


# Applicazione di mondrianAnon al dataset e salvataggio del risultato
result = mondrianAnon(small_dataset, ["zip-code", "education", "birthday"], 3)

# Scrive il risultato in un file CSV
output_file = "dataset-anonimized.csv"
write_to_csv(result, output_file)

print(f"Il risultato anonimizzato è stato scritto nel file '{output_file}'")