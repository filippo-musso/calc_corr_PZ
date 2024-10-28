import csv

def leggi_csv(file_path):
  with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    righe = [row for row in reader]
  return righe
