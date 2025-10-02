import os
import yaml
import pandas as pd

'''
Script om interface-elementen uit YAML-configuratiebestanden te extraheren en op te slaan in een CSV-bestand.
Het script doorloopt alle submappen in de opgegeven basisdirectory, leest de YAML-bestanden,
en verzamelt de gegevens in een DataFrame. Vervolgens wordt het resultaat weggeschreven naar een CSV-bestand.

Draai dit script in de root van de ETLocal repository.
'''

# Pad naar de map waar de YAML-bestanden staan
BASE_DIR = "config/interface_elements"

# Datum van vandaag in YYMMDD formaat
today = pd.Timestamp.now().strftime("%y%m%d")

# Lege lijst voor data
records = []

# Alle submappen en YAML-bestanden doorlopen
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".yml"):
            file_path = os.path.join(root, file)
            group = os.path.relpath(root, BASE_DIR).replace("\\", "/")  # Windows fix
            subgroup = os.path.splitext(file)[0]  # bestandsnaam zonder .yml

            # YAML-bestand laden
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f) or {}
                except yaml.YAMLError as e:
                    print(f"Fout in YAML-bestand {file_path}: {e}")
                    continue

            # We verwachten topniveau keys 'groups' en een hoofdsleutel 'key'
            groups = data.get("groups", [])

            # Door alle groepen heen
            for group_item in groups:
                items = group_item.get("items", [])
                for item in items:
                    item_key = item.get("key")
                    item_unit = item.get("unit", None)

                    if item_key:
                        records.append({
                            "group": group,
                            "subgroup": subgroup,
                            "key": item_key,
                            "unit": item_unit
                        })

# Alles in een DataFrame zetten
df = pd.DataFrame(records)

# Resultaat
print(df.head())

# Wegschrijven naar CSV
df.to_csv(f"{today}_etlocal_interface_elements.csv", index=False)
