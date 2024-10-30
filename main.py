import pandas as pd
import locale
from functions.caricamento_file import carica_loc_arco, carica_alta_urb_susa, carica_dis_susa

locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')

file_paths = {
    "Disagiate Arco": "./data/loc_disagiate_arco.csv",
    "Facchinaggio": "./data/loc_facchinaggio_arco.csv",
    "Balneari": "./data/loc_balneari_arco.csv",
    "Impervie": "./data/loc_impervie_arco.csv",
    "Disagiate Susa": "./data/loc_disagiate_susa.xlsx",
    "Alta Urbanizzazione": "./data/com_prov_susa.csv",
    "Tariffe": "./Q_TARIFFE_EXCEL.xlsx",
    "Tariffe Aggiunta": "./ESP_FATT.xlsx"
}

nomi_clienti = {
    903: "FM", 
    905: "Brugarolas", 
    908: "Cerutti", 
    917: "SetMar",
    921: "OilSa",
    924: "RAM",
    925: "AVService",
    927: "Stellantis Lombardia",
    934: "Maina",
    935: "Rossi",
    938: "IM",
    940: "Brandini",
    941: "EAA Oil",
    942: "CAF",
    944: "Stellantis Piemonte",
    945: "Andreini"
}

# Caricamento dei dati
disagiate_arco = carica_loc_arco(file_paths["Disagiate Arco"])
disagiate_susa = carica_dis_susa(file_paths["Disagiate Susa"])
facchinaggio = carica_loc_arco(file_paths["Facchinaggio"])
balneari = carica_loc_arco(file_paths["Balneari"])
impervie = carica_loc_arco(file_paths["Impervie"])
alta_urb = carica_alta_urb_susa(file_paths["Alta Urbanizzazione"])

# Caricamento del primo file Excel
df_tariffe = pd.read_excel(file_paths["Tariffe"])
df_fatt = pd.read_excel(file_paths["Tariffe Aggiunta"], parse_dates=[11], dtype={3: str, 7:str})

# Inizializzazione della lista per i dati da scrivere nel file di output
output_data = []

fac = False
bal = False
imp = False
urb = False

for index, row in df_tariffe.iterrows():
    num_doc = f"{row.iloc[0]}/{row.iloc[1]}"  # Formattazione numero/lettera

    for _, riga in df_fatt.iterrows():
        if num_doc == f"{riga.iloc[0]}/{riga.iloc[1]}":  # Confronto con il secondo file
            if riga['tm_coddest'] == 0:
                cap = riga['an_cap']
                loc = riga['an_citta']
                prov = riga['an_prov']
            else:
                cap = riga['dd_capdest']
                loc = riga['dd_locdest']
                prov = riga['dd_prodest']

            if riga['tm_vettor'] == 3:
                if (cap, loc, prov) in facchinaggio:
                    fac = True
                if (cap, loc, prov) in balneari: 
                    bal = True
                if (cap, loc, prov) in impervie:
                    imp = True
            if riga['tm_vettor'] == 946:
                if (cap, loc, prov) in alta_urb:
                    urb = True
            break

for index, row in df_tariffe.iterrows():
    num_doc = f"{row.iloc[0]}/{row.iloc[1]}"  # Formattazione numero/lettera

    nolo = row.iloc[7]
    tot = row.iloc[11]
    
    data_output = {
        "DOC": num_doc,
        "CLIENTE": row.iloc[2],  # Colonna 2
        "REGIONE": row.iloc[3],  # Colonna 3
        "PESO": row.iloc[4],     # Colonna 4
        "ARR.": row.iloc[5],     # Colonna 5
        "TAR.": row.iloc[6],     # Colonna 6
        "NOLO": round(row.iloc[7], 2),     # Colonna 7
        "TASS.": row.iloc[8],    # Colonna 8
        "ESPR.": row.iloc[9],     # Colonna 9
        "TEL.": row.iloc[10],     # Colonna 10
        "DIS.": 0,                # Inizialmente a 0
    }

    if fac == True:
        data_output["FAC."] = 0
    if bal == True:
        data_output["BAL."] = 0
    if imp == True:
        data_output["IMP."] = " "
    if urb == True:
        data_output["URB."] = 0

    # Calcolo Addebiti.
    for _, riga in df_fatt.iterrows():
        if num_doc == f"{riga.iloc[0]}/{riga.iloc[1]}":  # Confronto con il secondo file

            if riga['tm_coddest'] == 0:
                cap = riga['an_cap']
                loc = riga['an_citta']
                prov = riga['an_prov']
            else:
                cap = riga['dd_capdest']
                loc = riga['dd_locdest']
                prov = riga['dd_prodest']

            if riga['tm_vettor'] == 3:
                if (cap, loc, prov) in disagiate_arco:
                    arr = row.iloc[5]  # ARR.
                    data_output["DIS."] = ((arr + 100 - 1) // 100) * 4.50  # Calcolo
                    tot += data_output["DIS."]
                if (cap, loc, prov) in facchinaggio and fac == True:
                    data_output["FAC."] = ((arr + 100 - 1) // 100) * 6
                    tot += data_output["FAC."]
                if (cap, loc, prov) in balneari and bal == True:
                    data_output["BAL."] = round((nolo * 0.15), 2)
                    tot += data_output["BAL."]
                if (cap, loc, prov) in impervie and imp == True:
                    data_output["IMP."] = "IMP"
                

            elif riga['tm_vettor'] == 946:
                if (cap, loc, prov) in disagiate_susa:
                    arr = row.iloc[5]  # ARR.
                    data_output["DIS."] = ((arr + 100 - 1) // 100) * 4.50  # Calcolo
                    tot += data_output["DIS."]
                if (cap, loc, prov) in alta_urb and urb == True: 
                    data_output["URB."] = ((arr + 100 - 1) // 100) * 1.2
                    tot += data_output["URB."]

            data_output["TOTALE"] = round(tot, 2)

            break  # Esci dal ciclo una volta trovato il documento

    output_data.append(data_output)

# Creazione del DataFrame per il file di output
df_output = pd.DataFrame(output_data)

# Ricava il mese dalla data del documenta della prima riga delfile
data = df_fatt["tm_datadoc"].iloc[0]
mese_fatturazione = data.strftime("%B")

# Aggiunge il nome cliente in basa alla causale di magazzino, presa dalla prima riga del file
tm_causale = df_fatt["tm_causale"].iloc[0]
nome_cliente = nomi_clienti[tm_causale]

# Salvataggio del file di output
nome_file_output = f"Trasporto {nome_cliente} {mese_fatturazione}.xlsx"
df_output.to_excel(nome_file_output, index=False)

input(f"File di output creato: {nome_file_output}")
