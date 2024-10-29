import pandas as pd
from functions.caricamento_file import carica_loc_arco, carica_alta_urb_susa, carica_dis_susa

file_paths = {
    "Disagiate Arco": "./data/loc_disagiate_arco.csv",
    "Facchinaggio": "./data/loc_facchinaggio_arco.csv",
    "Balneari": "./data/loc_balneari_arco.csv",
    "Disagiate Susa": "./data/loc_disagiate_susa.xlsx",
    "Alta Urbanizzazione": "./data/com_prov_susa.csv",
    "Tariffe": "./Q_TARIFFE_EXCEL.xlsx",
    "Tariffe Aggiunta": "./ESP_FATT.xlsx"
}

# Caricamento dei dati
disagiate_arco = carica_loc_arco(file_paths["Disagiate Arco"])
disagiate_susa = carica_dis_susa(file_paths["Disagiate Susa"])

# Caricamento del primo file Excel
df_tariffe = pd.read_excel(file_paths["Tariffe"])
df_fatt = pd.read_excel(file_paths["Tariffe Aggiunta"], parse_dates=[11], dtype={3: str, 7:str})

# Inizializzazione della lista per i dati da scrivere nel file di output
output_data = []

# Formattazione mese corrente in italiano
import datetime
mese_corrente = datetime.datetime.now().strftime("%B")

for index, row in df_tariffe.iterrows():
    num_doc = f"{row.iloc[0]}/{row.iloc[1]}"  # Formattazione numero/lettera
    data_output = {
        "DOC": num_doc,
        "CLIENTE": row.iloc[2],  # Colonna 2
        "REGIONE": row.iloc[3],  # Colonna 3
        "PESO": row.iloc[4],     # Colonna 4
        "ARR.": row.iloc[5],     # Colonna 5
        "TAR.": row.iloc[6],     # Colonna 6
        "NOLO": row.iloc[7],     # Colonna 7
        "TASS.": row.iloc[8],    # Colonna 8
        "ESPR.": row.iloc[9],     # Colonna 9
        "TEL.": row.iloc[10],     # Colonna 10
        "DIS.": 0,                # Inizialmente a 0
        "TOTALE": row.iloc[11]    # Colonna 12
    }

    # Calcolo DIS.
    for _, riga in df_fatt.iterrows():
        if num_doc == f"{riga.iloc[0]}/{riga.iloc[1]}":  # Confronto con il secondo file
            tm_causale = riga['tm_causale']
            nome_cliente = "FM" if tm_causale == 903 else "Default"  # Default o altro valore se necessario

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
            elif riga['tm_vettor'] == 946:
                if (cap, loc, prov) in disagiate_susa:
                    arr = row.iloc[5]  # ARR.
                    data_output["DIS."] = ((arr + 100 - 1) // 100) * 4.50  # Calcolo
            break  # Esci dal ciclo una volta trovato il documento

    output_data.append(data_output)

# Creazione del DataFrame per il file di output
df_output = pd.DataFrame(output_data)

# Salvataggio del file di output
nome_file_output = f"Trasporto {nome_cliente} {mese_corrente}.xlsx"
df_output.to_excel(nome_file_output, index=False)

input(f"File di output creato: {nome_file_output}")
