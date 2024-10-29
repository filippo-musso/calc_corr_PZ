import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

def carica_loc_arco(file_path):
    # Carica il file CSV, forzando la prima colonna come stringa
    df = pd.read_csv(file_path, sep=';', header=None, dtype={0: str, 2:str})

    localita = []
    for index, row in df.iterrows():
        cap = row[0].strip()
        loc = row[1].strip().strip('"')
        prov = str(row[2]).strip()
        localita.append((cap, loc, prov))
    
    return localita

def carica_dis_susa(file_path):
    df = pd.read_excel(file_path, header=None, dtype={0: str})
    
    localita = []
    for index, row in df.iterrows():
        if row.iloc[4] in [3, 4]:
            cap = row.iloc[0].strip()
            loc = row.iloc[1].strip()
            prov = str(row.iloc[2]).strip()
            localita.append((cap, loc, prov))
    
    return localita

def carica_alta_urb_susa(file_path):
    # Carica il file CSV, forzando la prima colonna come stringa
    df = pd.read_csv(file_path, sep=';', header=None, dtype={0: str})

    localita = []
    for index, row in df.iterrows():
        cap = row[1].strip()
        loc = row[0].strip().strip('"')
        prov = str(row[2]).strip()
        localita.append((cap, loc, prov))
    
    return localita

def carica_file_fatturazione(file_path):
  df = pd.read_excel(file_path, header=None, dtype={3: str, 7:str})
  data = df.values.tolist()
  return data