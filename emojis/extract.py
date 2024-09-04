import pandas as pd

## Inital dataset : https://www.kaggle.com/code/subinium/emoji-full-emoji-dataset

# Charger le DataFrame depuis le fichier CSV
emoji = pd.read_csv('./full_emoji.csv')

# Sélectionner les colonnes 0, 1 et 3
selected_columns = emoji.iloc[:, [0, 1, 3]]

# Exporter les colonnes sélectionnées dans un nouveau fichier CSV
selected_columns.to_csv('./selected_emoji_columns.csv', index=False)
