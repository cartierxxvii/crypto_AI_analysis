import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import glob

def prepare_data(data_folder, sequence_length=50):
    """
    Charge toutes les données collectées et les prépare pour l'entraînement.
    :param data_folder: Chemin vers le dossier contenant les fichiers CSV.
    :param sequence_length: Longueur des séquences pour le modèle.
    :return: X (features), y (targets), scaler utilisé pour normaliser.
    """
    all_files = glob.glob(f"{data_folder}/*.csv")
    all_data = []

    # Charger les données de chaque fichier CSV
    for file in all_files:
        df = pd.read_csv(file)
        if "close" in df.columns:  # Vérifiez que la colonne 'close' existe
            all_data.extend(df["close"].values.tolist())

    # Convertir en DataFrame et normaliser
    all_data = pd.DataFrame(all_data, columns=["close"])
    scaler = MinMaxScaler(feature_range=(0, 1))
    normalized_data = scaler.fit_transform(all_data)

    # Créer des séquences
    X, y = [], []
    for i in range(len(normalized_data) - sequence_length):
        X.append(normalized_data[i:i+sequence_length])
        y.append(normalized_data[i+sequence_length])

    return np.array(X), np.array(y), scaler