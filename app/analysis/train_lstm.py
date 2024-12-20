import os
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from app.analysis.data_preparation import prepare_data

# Paramètres
DATA_FOLDER = "data"  # Chemin vers le dossier contenant les fichiers CSV
SEQUENCE_LENGTH = 50
EPOCHS = 50
BATCH_SIZE = 32
MODEL_PATH = "models/lstm_model.keras"
TRAINED_FILES_LOG = "trained_files.log"

# Charger la liste des fichiers déjà utilisés
def load_trained_files_log(log_path):
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            return set(f.read().splitlines())
    return set()

# Sauvegarder la liste des fichiers déjà utilisés
def save_trained_files_log(log_path, trained_files):
    with open(log_path, "w") as f:
        f.write("\n".join(trained_files))

# Charger les fichiers déjà utilisés
trained_files = load_trained_files_log(TRAINED_FILES_LOG)

# Charger et préparer les nouvelles données
print("Chargement et préparation des données...")
X, y, scaler, new_files = prepare_data(DATA_FOLDER, sequence_length=SEQUENCE_LENGTH, exclude_files=trained_files)

# Vérifier si de nouvelles données existent
if not new_files:
    print("Aucune nouvelle donnée à entraîner. Fin du script.")
    exit()

print(f"Fichiers ajoutés : {new_files}")
print(f"Dimensions des données : X={X.shape}, y={y.shape}")

# Charger le modèle existant ou en créer un nouveau
if os.path.exists(MODEL_PATH):
    print("Chargement du modèle existant...")
    model = load_model(MODEL_PATH)
else:
    print("Construction d'un nouveau modèle LSTM...")
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(SEQUENCE_LENGTH, 1)),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25, activation="relu"),
        Dense(1)
    ])
    model.compile(optimizer="adam", loss="mean_squared_error")
    print(model.summary())

# Entraîner le modèle
print("Début de l'entraînement...")
early_stopping = EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)

history = model.fit(
    X, y,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    callbacks=[early_stopping],
    verbose=1
)

# Sauvegarder le modèle
print(f"Sauvegarde du modèle dans {MODEL_PATH}...")
model.save(MODEL_PATH)

# Mettre à jour la liste des fichiers déjà utilisés
trained_files.update(new_files)
save_trained_files_log(TRAINED_FILES_LOG, trained_files)

print("Entraînement terminé et modèle sauvegardé.")