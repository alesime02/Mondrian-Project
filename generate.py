import random
from faker import Faker
import datetime
import csv

# random.seed(42)

fake = Faker('it_IT')
political_parties = ["Partito Democratico", "Movimento 5 Stelle", "Lega Nord", "Fratelli di Italia", "Verdi",
                     "Forza Italia", "Italia Viva", "Azione", "EuropaVerde", "Sinistra Italiana", "NoiModerati",
                     "Unione di centro", "Coraggio Italia", "PiuEuropa", "Democrazia solidale", "Partito Comunista dei Lavoratori",
                     "Radicali Italiani", "Nuovo PSI", "Centro Democratico", "Centristi per l'Europa", "Movimento Animalista"]
religion = ["Ateo", "Cristianesimo", "Islam", "Buddhismo", "Induismo", "Confucianesimo", "Shintoismo"]

education = ["elementary schools", "middle schools", "high schools", "bachelor degree", "master degree", "phd"]
genders = ["M", "F", "O", "N/D"]

# Definizione dei pesi per ciascun livello di istruzione
education_weights = [0.3, 0.3, 0.25, 0.05, 0.08, 0.02]

def generateDataset(n = 1000, filename = None):
    generated = []
    for i in range(n):
        entry = {
            "id": i,
            "name": fake.name(),
            "birthday": datetime.date(random.randint(1930, 2006), random.randint(1, 12), random.randint(1, 28)),
            "zip-code": random.randint(16010, 16167),
            "education": random.choices(education, weights=education_weights, k=1)[0],
            "gender": random.choice(genders),
            "salary": random.randint(12000, 120000),
            "favorite-party": random.choice(political_parties),
            "religion": random.choice(religion)
        }
        generated.append(entry)

    if filename is not None:
        with open(filename, 'w') as csvfile:
            fieldnames = [
                "id",
                "name",
                "birthday",
                "zip-code",
                "education",
                "gender",
                "salary",
                "favorite-party",
                "religion"
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in generated:
                writer.writerow(row)

    return generated

#generateDataset(n = 33, filename = "dataset2.csv")
#generateDataset(n = 1000, filename="dataset.csv")
#generateDataset(n = 12, filename="dataset-small.csv")
generateDataset(n = 100000, filename="dataset-big.csv")