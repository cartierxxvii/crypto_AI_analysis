import pandas as pd
import pandas_ta as ta

class TechnicalIndicators:
    @staticmethod
    def calculate_rsi(prices, period=14):
        """
        Calcule le RSI (Relative Strength Index).
        :param prices: Liste ou Series des prix.
        :param period: Période pour le RSI (par défaut 14).
        :return: DataFrame avec les valeurs RSI.
        """
        df = pd.DataFrame(prices, columns=["close"])
        df["RSI"] = ta.rsi(df["close"], length=period)

        # Remplir les valeurs manquantes avec 0
        df["RSI"] = df["RSI"].fillna(0)

        return df

    @staticmethod
    def calculate_macd(prices, fast=12, slow=26, signal=9):
        """
        Calcule le MACD (Moving Average Convergence Divergence).
        :param prices: Liste ou Series des prix.
        :param fast: Période rapide (par défaut 12).
        :param slow: Période lente (par défaut 26).
        :param signal: Période de la ligne de signal (par défaut 9).
        :return: DataFrame avec les colonnes MACD, Signal, Histogram.
        """
        # Création du DataFrame des prix
        df = pd.DataFrame(prices, columns=["close"])

        # Calcul du MACD
        macd = ta.macd(df["close"], fast=fast, slow=slow, signal=signal)

        # Vérification si `macd` est None ou vide
        if macd is None or macd.empty:
            raise ValueError("Le calcul du MACD a échoué. Vérifiez les données d'entrée.")

        # Ajouter les colonnes générées au DataFrame principal
        df = pd.concat([df, macd], axis=1)

        # Remplir les valeurs nulles avec des 0
        for col in ["MACD_12_26_9", "MACDs_12_26_9", "MACDh_12_26_9"]:
            if col in df:
                df[col] = df[col].fillna(0)

        # Renommer les colonnes pour une meilleure lisibilité
        df.rename(columns={
            "MACD_12_26_9": "MACD",
            "MACDs_12_26_9": "Signal",
            "MACDh_12_26_9": "Histogram"
        }, inplace=True)

        # Vérification finale des colonnes
        for col in ["MACD", "Signal", "Histogram"]:
            if col not in df or df[col].isnull().all():
                raise ValueError(f"Le calcul du MACD contient des valeurs invalides dans la colonne {col}.")

        # Remplir les valeurs manquantes avec des 0 après le renommage
        df["MACD"] = df["MACD"].fillna(0)
        df["Signal"] = df["Signal"].fillna(0)
        df["Histogram"] = df["Histogram"].fillna(0)

        return df[["close", "MACD", "Signal", "Histogram"]]