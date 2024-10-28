import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.csv_reader import leggi_csv

def carica_loc_arco(file_path):
  localita = []
  righe = leggi_csv(file_path)

  for row in righe: 
    if len(row) >= 3: 
      cap = str(row[0].strip())
      loc = row[1].strip().strip('"')
      prov = row[2].strip()
      localita.append((cap, loc, prov))
    else:
      print(f"Riga ignorata (non abbastanza colonne): {row}\n\n")