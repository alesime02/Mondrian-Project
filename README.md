# Mondrian K-Anonymity Implementation
## L. Galleano, A. Simeoni, E. G. M. Valente
##### DIBRIS - Università degli Studi di Genova - Data Protection and Privacy - Exam Project

This project implements the Mondrian algorithm, a spatial partitioning technique for achieving k-anonymity on datasets containing sensitive information. The algorithm generalizes identifying attributes (Quasi-Identifiers) to protect the privacy of individuals in the dataset.
The whole project has been done following [the paper](https://pages.cs.wisc.edu/~lefevre/MultiDim.pdf).

## Features
This repository includes the following files:
- `generate.py` provides functionality to create realistic synthetic demographic datasets for testing and development purposes, specifically tailored to Italian context with possibility to control the randomization of the attributes. The table obtained is like this:

| id | name                   | birthday   | zip-code | education      | gender | salary | favorite-party      | religion       |
|----|------------------------|------------|----------|----------------|--------|--------|---------------------|----------------|
|    |                        |            |          |                |        |        |                     |                |
| 0  | Eraldo Canali-Tencalla | 1985-07-16 | 16159    | master degree  | N/D    | 107477 | Italia Viva         | Confucianesimo |
|    |                        |            |          |                |        |        |                     |                |
| 1  | Sig. Amleto Mercantini | 1974-10-13 | 16164    | high schools   | M      | 108381 | Azione              | Confucianesimo |
|    |                        |            |          |                |        |        |                     |                |
| 2  | Alphons Quasimodo      | 1952-12-20 | 16078    | middle schools | N/D    | 100801 | Democrazia solidale | Shintoismo     |
|    |                        |            |          |                |        |        |                     |                |
| 3  | Dott. Gloria Carnera   | 1997-10-13 | 16071    | middle schools | N/D    | 67218  | Nuovo PSI           | Cristianesimo  |

- `generalize.py` provides essential functions for data anonymization, featuring one-way tokenization of sensitive identifiers and a hierarchical structure for educational attribute generalization.
- `kanon.py` provides a simple test which takes a table and returns true if it is randomized, false otherwise.
- `mondrian.py` contains the actual code and can be used as entry point.
- `mondrian_function.py` provides a wrapper of functions used in `mondrian.py`.
We also include our test file and our result:
- `dataset.csv` is the original dataset `generate.py` returned.
- `dataset_anonymized` is the result of our implementation.

## Installation
Clone this repository:
```bash
git clone https://github.com/alesime02/Mondrian-Project
cd Mondrian-Project
```
Then install `faker` in order to use the generator of realistic randomized data:
```bash
pip install faker
```
Install also `numpy` which is needed in order to install `plotly`. This last one was used in order to have final metrics plotted on screen:
```bash
pip install numpy
pip install plotly
```

## Usage
Run using:
```bash
python main_script.py
```
