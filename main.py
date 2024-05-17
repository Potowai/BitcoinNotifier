import requests
import time
import customtkinter as ctk
import threading

# Constantes
TIME_TO_SLEEP = 15  # secondes
API_URL = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur'
CUSTOM_FONT = ("Helvetica", 16, "bold")

class BitcoinPriceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bitcoin Price Notifier")
        self.geometry("400x70")

        self.label = ctk.CTkLabel(self, text="Prix du Bitcoin : Récupération en cours...", font=CUSTOM_FONT)
        self.label.pack(pady=20)

        self.initial_price = None
        self.previous_price = None

        self.update_price()  # Appel initial pour récupérer le prix
        self.start_updating()  # Démarrer le thread pour mise à jour en direct

    def get_bitcoin_price(self):
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            data = response.json()
            price = data["bitcoin"]["eur"]
            return price
        except (requests.RequestException, KeyError):
            return None

    def update_price(self):
        current_price = self.get_bitcoin_price()
        if current_price is not None:
            if self.initial_price is None:
                self.initial_price = current_price

            change = current_price - self.initial_price
            if change > 0:
                color = "green"
                change_text = f"(↑ {change}€ depuis le lancement)"
            elif change < 0:
                color = "red"
                change_text = f"(↓ {-change}€ depuis le lancement)"
            else:
                color = "black"
                change_text = "(→ 0€ depuis le lancement)"
            
            self.label.configure(text=f"Prix du Bitcoin : {current_price}€ {change_text}", text_color=color)
            self.previous_price = current_price
        else:
            self.label.configure(text="Erreur lors de la récupération du prix", text_color="black")

    def start_updating(self):
        def update_loop():
            while True:
                self.update_price()
                time.sleep(TIME_TO_SLEEP)

        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()

if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # Utiliser le mode d'apparence clair
    ctk.set_default_color_theme("blue")  # Utiliser le thème de couleur bleu
    app = BitcoinPriceApp()
    app.mainloop()
