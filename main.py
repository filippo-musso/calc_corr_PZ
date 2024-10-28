from functions.caricamento_file import carica_loc_arco, carica_alta_urb_susa, carica_dis_susa, carica_file_fatturazione

file_paths = {
  "Disagiate Arco": "./data/loc_disagiate_arco.csv", 
  "Facchinaggio": "./data/loc_facchinaggio_arco.csv",
  "Balneari": "./data/loc_balneari_arco.csv",
  "Disagiate Susa": "./data/loc_disagiate_susa.xlsx",
  "Alta Urbanizzazione": "./data/com_prov_susa.csv",
  "Tariffe": "./Q_TARIFFE_EXCEL.xlsx", 
  "Tariffe Aggiunta": "./ESP_FATT.xlsx"
}

for label, file_path in file_paths.items():
  if label == "Disagiate Arco":
    disagiate_arco = carica_loc_arco(file_path)
  if label == "Facchinaggio":
    facchinaggio = carica_loc_arco(file_path)
  if label == "Balneari":
    balneari = carica_loc_arco(file_path)
  if label == "Disagiate Susa":
    disagiate_susa = carica_dis_susa(file_path)
  if label == "Alta Urbanizzazione":
    alta_urb = carica_alta_urb_susa(file_path)
  if label == "Tariffe":
    tariffe = carica_file_fatturazione(file_path)
  if label == "Tariffe Aggiunta":
    aggiunta_tar = carica_file_fatturazione(file_path)

header1 = ["DOC", "CLIENTE", "REGIONE", "PESO", "ARR.", "TAR.", "NOLO", "TASS.", "ESPR.", "TEL.", "DIS.", "TOTALE"]
header2 = ["DOC", "CLIENTE", "ADDEBITO", "TOTALE"]

for row in tariffe:
  num_doc = str(row[0]) + "/" + row[1]
  print(num_doc)
  

