import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from utils.csv_reader import leggi_csv

def carica_loc_arco(file_path):
  localita = []
  righe = leggi_csv(file_path)

  for row in righe: 
    cap = str(row[0]).strip()
    loc = row[1].strip().strip('"')
    prov = row[2].strip()
    localita.append((cap, loc, prov))
  
  return localita

def carica_dis_susa(file_path):
  df = pd.read_excel(file_path, header=None)
  
  localita = []

  for index, row in df.iterrows():
    if row.iloc[4] in [3, 4]:
      cap = str(row.iloc[0]).strip()
      loc = row.iloc[1].strip()
      prov = str(row.iloc[2]).strip()
      localita.append((cap, loc, prov))
    
  return localita

def carica_alta_urb_susa(file_path):
  localita = []
  righe = leggi_csv(file_path)

  for row in righe:
    cap = str(row[1]).strip()
    loc = row[0].strip().strip('"')
    prov = row[2].strip()
    localita.append((cap, loc, prov))
  
  return localita

def carica_file_fatturazione(file_path):
  df = pd.read_excel(file_path, header=None)
  data = df.values.tolist()
  return data