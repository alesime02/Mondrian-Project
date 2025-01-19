import plotly.express as px
import generalize as gen
import csv
import os

education_list = list(gen.education_tree)

def plot_graph(input_on_x, input_on_y, title, x_name, y_name, graph_hover_name_x, graph_hover_name_y):
    fig1 = px.line(x=input_on_x, y=input_on_y, width=800, height=500, labels={'x': graph_hover_name_x, 'y':graph_hover_name_y})
    fig1.update_traces(line=dict(color='royalblue', width=3, dash='solid'))
    fig1.update_layout(
    title=dict(
        text=title,
        font=dict(size=24, color="darkblue"),
        x=0.5,
    ),
    xaxis=dict(
        title=x_name,
        titlefont=dict(size=18, color="darkblue"),
        tickfont=dict(size=14, color="black"),
        showgrid=True, 
        gridcolor="lightgray",
    ),
    yaxis=dict(
        title=y_name,
        titlefont=dict(size=18, color="darkblue"),
        tickfont=dict(size=14, color="black"),
        showgrid=True,  
        gridcolor="lightgray",
    ),
    plot_bgcolor="white",
    paper_bgcolor="lightgray",  
    legend=dict(
        title="Legenda",
        font=dict(size=14, color="darkblue"),
    ),
    )
    return fig1

# Dataset opening from .csv file
def read_csv_if_exists(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return list(csv.DictReader(f))
    else:
        print(f"File '{filename}' not found.")
        return None

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