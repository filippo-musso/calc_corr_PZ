from functions.loc_arco import carica_loc_arco

file_paths = {
  "Disagiate Arco": "../data/loc_disagiate_arco.csv", 
  "Facchinaggio": "../data/loc_facchinaggio_arco.csv",
  "Balneari": "../data/loc_balneari_arco.csv"
}

for label, file_path in file_paths.items():
  if label == "Disagiate Arco":
    disagiate = carica_loc_arco(file_path)
  if label == "Facchinaggio":
    facchinaggio = carica_loc_arco(file_path)
  if label == "Balneari":
    balneari = carica_loc_arco(file_path)

