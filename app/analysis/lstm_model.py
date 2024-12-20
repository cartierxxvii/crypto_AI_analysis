import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import ModelCheckpoint

class LSTMModel:
    def __init__(self, input_shape):
        """
        Initialise un modèle LSTM avec la forme d'entrée spécifiée.
        """
        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=input_shape),
            tf.keras.layers.LSTM(50, return_sequences=True),
            tf.keras.layers.LSTM(50),
            tf.keras.layers.Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def train(self, X_train, y_train, X_val, y_val, epochs=10, batch_size=32, checkpoint_path="models/lstm_checkpoint.h5"):
        """
        Entraîne le modèle LSTM sur les données spécifiées avec gestion des checkpoints.
        """
        # Callback pour sauvegarder les checkpoints
        checkpoint_callback = ModelCheckpoint(
            filepath=checkpoint_path,
            save_best_only=True,
            monitor="val_loss",
            mode="min",
            verbose=1
        )

        # Entraînement du modèle avec les callbacks
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[checkpoint_callback]  # Ajout du callback
        )
        return history

    def predict(self, X):
        """
        Fait des prédictions à l'aide du modèle.
        """
        return self.model.predict(X)

    def save_model(self, path):
        """
        Sauvegarde le modèle dans le chemin spécifié.
        """
        self.model.save(path)
        print(f"Modèle sauvegardé dans le fichier : {path}")

    def load_model(self, path):
        """
        Charge un modèle depuis le chemin spécifié.
        """
        self.model = tf.keras.models.load_model(path)
        print(f"Modèle chargé depuis le fichier : {path}")

    @staticmethod
    def train_model(model, X_train, y_train, X_val, y_val, epochs=50, batch_size=32, checkpoint_path="models/lstm_checkpoint.h5"):
        """
        Méthode statique pour entraîner un modèle avec gestion des checkpoints.
        """
        # Callback pour sauvegarder les checkpoints
        checkpoint_callback = ModelCheckpoint(
            filepath=checkpoint_path,
            save_best_only=True,
            monitor="val_loss",
            mode="min",
            verbose=1
        )

        # Entraînement du modèle avec les callbacks
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[checkpoint_callback]
        )
        return model, history