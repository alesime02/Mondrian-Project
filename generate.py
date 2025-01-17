import random
from faker import Faker
import datetime
import csv

# random.seed(42)


# Categorical attributes
cities = ["Genova", "Milano", "Rome"]
contries = ["Italy", "Germany", "France", "..."]

#print(cities[random.randint(0, len(cities)-1)])
print(random.choices(cities, weights=[2, 10, 12], k = 10))

# Numerical attributes

# Integer numerical attributes
print(random.randint(1, 100))
print(random.randint(1, 100))
print(random.randint(1, 100))
print(random.randint(0, 99))

# Real numerical attributes
print(random.random() * 100)

fake = Faker('it_IT')
for _ in range(10):
    print(fake.name())

'''
ID (number, incremental, unique) <- EI 
name, surname <- EI (string, categorical)

birthday <- QI      (number)       01/01/1930 - 31/12/2023
country <- QI       (categorical)  [list of countries]
Zip code <- QI      (number)       16121 - 16167
gender <- QI        (categorical)  [list of genders]
education <- QI     (categorical)  [list of education]

salary <- SD        (real number)        0 - 1000000
height <- SD        (number)        120 - 200
weight <- SD        (number)        40 - 150
condition <- SD     (categorical)   [list condition]
'''

medial_conditions = ["hearth disease", "flu", "stomach", "headache", "backpain", "broken bones"]
education = ["elementary schools", "middle schools", "high schools", "bachelor degree", "master degree", "phd"]
genders = ["M", "F", "O", "N/D"]

def generateDataset(n = 1000, filename = None):
    generated = []
    for i in range(n):
        entry = {
            "id": i,
            "name": fake.name(),
            "birthday": datetime.date(random.randint(1930, 2023), random.randint(1, 12), random.randint(1, 28)),
            "country": fake.country(),
            "zip-code": random.randint(16121, 16167),
            "gender": random.choice(genders),
            "education": random.choice(education),
            "salary": random.random() * 1000000,
            "height": random.randint(120, 200),
            "weight": random.randint(40, 150),
            "condition": random.choice(medial_conditions)
        }
        generated.append(entry)

    if filename is not None:
        with open(filename, 'w') as csvfile:
            fieldnames = [
                "id",
                "name",
                "birthday",
                "country",
                "zip-code",
                "gender",
                "education",
                "salary",
                "height",
                "weight",
                "condition"
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in generated:
                writer.writerow(row)

    return generated

generateDataset(n = 1000, filename="dataset.csv")

generateDataset(n = 12, filename="dataset-small.csv")