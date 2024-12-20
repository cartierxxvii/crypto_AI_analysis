class Strategy:
    @staticmethod
    def calculate_entry(price, stop_loss_percentage, take_profit_percentage):
        """Calcule les niveaux d'entrée, Stop-Loss et Take-Profit."""
        stop_loss = price - (price * stop_loss_percentage / 100)
        take_profit = price + (price * take_profit_percentage / 100)
        return {
            "entry": price,
            "stop_loss": stop_loss,
            "take_profit": take_profit
        }