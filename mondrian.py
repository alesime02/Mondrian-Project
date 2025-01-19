from kanon import is_k_anon
import generalize as gen
import mondrian_functions as mf

education_list = list(gen.education_tree)

# Generalizes a dataset, in the algorithm it is used to generalize the union of LHS and RHS.
def summarize(dataset, QIs):
    for qi in QIs:
        if(qi == "birthday"):
            for row in dataset:
                row[qi] = row[qi].split("-")[0]
            # Dataset sorting
            dataset.sort(key=lambda x: x[qi])
            # generalized range for the attribute
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
    maxQI = mf.find_best_attribute(dataset, QIs)
    # fs ← frequency set(partition, dim)
    fs = mf.frequency_set(dataset, maxQI)
    # splitVal ← find median(fs)
    splitVal = mf.find_median_in_fs(fs, maxQI)
    # lhs ← {t ∈ partition : t.dim ≤ splitVal}
    LHS = [row for row in dataset if row[maxQI] <= splitVal]
    # rhs ← {t ∈ partition : t.dim > splitVal}
    RHS = [row for row in dataset if row[maxQI] > splitVal]

    # If both parts are greater than K, is still possible to cut the partition
    if((len(LHS) >= K) and (len(RHS) >= K)):
        return mondrianAnon(LHS, QIs, K) + mondrianAnon(RHS, QIs, K)
    
    # return Anonymize(rhs) ∪ Anonymize(lhs)
    return summarize((LHS+RHS), QIs)





# ---------------------------------------------------------------------------------------
# Reading dataset
dataset = None
dataset = mf.read_csv_if_exists("dataset.csv")
if (dataset == None):
    exit()
# ---------------------------------------------------------------------------------------





# ---------------------------------------------------------------------------------------
# Result computation and parameters' setting
k = 5
QIs = ["zip-code", "education", "birthday","gender"]
EIs = ["id", "name"]

# If attributes are not in dataset, quit
if(not set(EIs + QIs).issubset(dataset[0].keys())):
    print("Invalid attributes.")
    exit()

tokenized_dataset = gen.tokenize_dataset(dataset, EIs)
result = mondrianAnon(tokenized_dataset, QIs, k)
# ---------------------------------------------------------------------------------------





# ---------------------------------------------------------------------------------------
# Quality results
num_equivalence_classes = mf.count_equivalence_classes(result, QIs)
C_avg = (len(dataset) / num_equivalence_classes) / k
upperbound = ((2 * len(QIs) * (k-1)) + num_equivalence_classes)/k
if(is_k_anon(result, QIs, k)):
    print("The table is "+str(k)+"-anonymous")
print("Number of equivalence classes: " + str(num_equivalence_classes))
print("Normalized average equivalence class size metric (C_avg): " + str(C_avg))
print("Upperbound to respect: " + str(C_avg) + " <= " + str(upperbound))
# ---------------------------------------------------------------------------------------





# ---------------------------------------------------------------------------------------
# Plot C_avg in function of k
k_values = range(1, 1001)
C_avg_values = []
for k_for_plot in k_values:
    result_for_plot = mondrianAnon(dataset, QIs, k_for_plot)
    num_equivalence_classes_for_plot = mf.count_equivalence_classes(result_for_plot, QIs)
    C_avg_for_plot = (len(dataset) / num_equivalence_classes_for_plot) / k_for_plot
    C_avg_values.append(C_avg_for_plot)

fig1 = mf.plot_graph(k_values, C_avg_values, "k values wrt c_avg values", "k values", "C_avg values")
fig1.show()
# ---------------------------------------------------------------------------------------





# ---------------------------------------------------------------------------------------
# Writes the result in a .csv file
output_file = "dataset-anonimized.csv"
mf.write_to_csv(result, output_file)
print(f"The resultant table is exported in: '{output_file}'")
# ---------------------------------------------------------------------------------------