from sklearn.linear_model import LinearRegression

class AIModel:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, X, y):
        """Entraîne le modèle IA avec les données."""
        self.model.fit(X, y)

    def predict(self, X):
        """Retourne les prédictions du modèle."""
        return self.model.predict(X)