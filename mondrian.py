from kanon import is_k_anon
import generalize as gen
import csv
sequence = [1, 2, 2, 3, 4, 4, 4, 5, 6, 7, 8, 9, 9, 9, 9, 10, 11, 12, 13]

'''
1, 2, 3     <- % 2 = 1    -> median = 2
1, 2, 3, 4  <- % 2 = 0    -> median = (2+3) / 2 = 2.5
'''

def median(sequence):
    sequence = list(sorted(sequence))
    median = -1
    if len(sequence) % 2 == 0:
        median = ( sequence[ len(sequence) // 2 -1 ] + sequence[ len(sequence) // 2 ] ) /2
    else:
        median = sequence[ len(sequence) // 2 ]
    return median

def median2(sequence):
    sequence = list(sorted(sequence))
    return sequence[ len(sequence) // 2 ]

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

'''
if(qi == "zip-code"):
            for row in dataset:
                row[qi] = gen.myGeneralizeNumbers(row[qi])
        if(qi == "birthday"):
            for row in dataset:
                row[qi] = gen.age_generalization(row[qi])
        if(qi == "education"):
            for row in dataset:
                row[qi] = gen.generalize_function(row[qi])
'''

'''
sembra ok ma bisogna sistemare come vengono generalizzati i cathegorical attributes, a grandi linee bisogan generalizzare solo nell'ultima partizione che si ottiene finché quella partizione non è k anonima, in questo modo mi vado a costruire tanti blocchi q* k-anonimi che poi compongono la tabella rendendola k-anonima, che te ne pare? siamo aperti a critiche e revisioni, abbiamo anche pasticciato nel codice e cagato in giro
Cordiali saluti, Ale e Livio

'''

def summarize(dataset, QIs):
    for qi in QIs:
        # Ordina il dataset in base alla chiave specificata (qi)
        dataset.sort(key=lambda x: x[qi])
        # Calcola l'intervallo generalizzato per la colonna
        min_value = dataset[0][qi]
        max_value = dataset[-1][qi]
        generalized_value = f"[{min_value} - {max_value}]"
        # Sostituisci il valore nella colonna con l'intervallo generalizzato
        for row in dataset:
            row[qi] = generalized_value
    return dataset

# Makes the dataset k-anonymous by
# generalizing QIs
def mondrianAnon(dataset, QIs, K):

#a questo punto penso che questo si possa togliere
    # TODO: Check if dataset in already K anonymous
    if (is_k_anon(dataset, QIs, K)):
        return dataset
    # If true stop
    
    # I don't have any new quasi identifiers to generalize
    # in order to reach k-anonymization
    #if len(QIs) == 0:
    #   return dataset
    # I have some quasi-identifier to generalize
    else:
        # dim ← choose dimension()
        # ^ choose one elements inside QIs to split my dataset
        dim = QIs[0]
        maxQI = ""
        maxdim = 0
        
        # choose the QI with the most different values 
        values = []
        for QI in QIs:
            # This will create a set with all the distinct values
            # for the currenct quasi-identifier
            values.append( len( set( row[QI] for row in dataset)) )
            if(values[-1] > maxdim):
                maxdim = values[-1]
                maxQI = QI
            
        # maxQI è l'attributo con il maggior numero di valori unici
        # values è una lista che contiene quanti elementi unici ci sono in un attributo
        
        # Takes the first element that has the maximum diverse values
        # inside the dataset
        dim = values[values.index(max(values))]

        '''
        dataset = {
            ZIP CODE = [3, 3, 4, 5, 5, 5, 6, 7, 7, 7, 9] <- set(3, 4, 5, 6, 7, 9) <- 6
            CITY     = [A, A, A, A, B, B, B, B, B, E, E] <- set(A, B, E)          <- 3
            DEGREE   = [B, B, B, B, P, P, P, M, M, H, H] <- set(B, P, M, H)       <- 4
        }
        '''

        #f s ← frequency set(partition, dim)
        #splitV al ← ﬁnd median(f s)
        # ^ find the median value for the choosen attribute (dim)
        medValue = int
        
        # Get the median value for splitting
    values = sorted(set(row[maxQI] for row in dataset))
    if isinstance(values[0], (int, float)):
        # Numerical median
        medValue = median2(values)
    else:
        # Categorical "median" (use frequency-based split or mid-point)
        medValue = median2(values)
        '''if(maxQI == "country"):
            all_values_in_QI = [row[maxQI] for row in dataset]
            medValue = median2(all_values_in_QI)'''
        
        #lhs ← {t ∈ partition : t.dim ≤ splitV all}
        #rhs ← {t ∈ partition : t.dim > splitV all}
        # ^ split dataset in two partition
        # LHS <- all the elements <= median
        # RHS <- all the elements > median
        # Split the dataset into two partitions
        print("Median value: " + str(medValue) + "\n")


        '''
        creo le partizioni, se sono di dimensioni maggiore o uguale a k, alla vuol dire che posso andare avanti a partizionare quindi
        faccio le due chiamate ricorsive, la ricorsione mi ritorna dei dataset con almeno k righe generalizzate una volta, perché questo fa
        la funzione summarize, quindi i dati vengono generalizzati una volta per ogni ritorno da chiamata ricorsiva
        quando non posso più partizionare allora viene chiamata summarize che generalizza la partizione corrente e la ritorna


        '''
        
        LHS = [row for row in dataset if row[maxQI] <= medValue]
        RHS = [row for row in dataset if row[maxQI] > medValue]
        print("LHS: "+str(LHS) + "\n")
        print("RHS: "+str(RHS) + "\n")
        if((len(LHS) >= K) and (len(RHS) >= K)):
            return mondrianAnon(LHS, QIs, K) + mondrianAnon(RHS, QIs, K)
        return summarize((LHS+RHS), QIs)
        # TODO: Generalize LHS and RHS according to the previous example


        # Remove the used attributes from the available list
        #QIsNew = [q for q in QIs if q != maxQI]
        
        #return Anonymize(lhs) ∪ Anonymize(rhs)
         
    

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
result = mondrianAnon(small_dataset, ["zip-code", "education"], 3)

# Scrive il risultato in un file CSV
output_file = "dataset-anonimized.csv"
write_to_csv(result, output_file)

print(f"Il risultato anonimizzato è stato scritto nel file '{output_file}'")




'''



generalize and split by city

mondrian(LHS, [zip code, degree], 3) + mondrian(RHS, [zip code, degree], 3)

generalize and split by zip code

mondrian(LHS1, [degree], 3) + mondrian(LHS2, [degree], 3) + ...

generalize and split by degree level

mondrian(LHS11, [], 3) + 


'''
        