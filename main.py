import requests
import time
import customtkinter as ctk
import threading
from settings import *

# Constantes
TIME_TO_SLEEP = 15  # secondes
API_URL_CURRENT = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur'
CUSTOM_FONT = ("Helvetica", 16, "bold")
PERCENTAGE_FONT = ("Helvetica", 12, "bold")

class BitcoinPriceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        print("Initialisation de l'application...")
        self.title("")
        self.iconbitmap(EMPTY_ICON)
        self.geometry("450x150")
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')  # Centrer la fenêtre

        self.current_price_label = ctk.CTkLabel(self, text="Prix du Bitcoin : Récupération en cours...", font=CUSTOM_FONT)
        self.current_price_label.pack(pady=(10, 0))

        self.change_label = ctk.CTkLabel(self, text="", font=CUSTOM_FONT)
        self.change_label.pack(pady=(10, 0))

        self.percentage_label = ctk.CTkLabel(self, font=PERCENTAGE_FONT)
        self.percentage_label.pack(pady=(10, 10))

        self.initial_price = None
        self.previous_price = None
        self.price_24h_ago = None

        self.update_price()  # Appel initial pour récupérer le prix
        self.start_updating()  # Démarrer le thread pour mise à jour en direct

    def get_bitcoin_price(self):
        try:
            response = requests.get(API_URL_CURRENT)
            response.raise_for_status()
            data = response.json()
            price = data["bitcoin"]["eur"]
            return price
        except (requests.RequestException, KeyError):
            return None

    def get_bitcoin_details(self):
        try:
            response = requests.get(API_URL_DETAILS)
            response.raise_for_status()
            data = response.json()
            price_24h_ago = data["market_data"]["current_price"]["eur"]
            return price_24h_ago
        except (requests.RequestException, KeyError):
            return None

    def update_price(self):
        current_price = self.get_bitcoin_price()
        if self.price_24h_ago is None:
            self.price_24h_ago = self.get_bitcoin_details()

        color = "white"
        if current_price is not None and self.price_24h_ago is not None:
            percentage_change = ((current_price - self.price_24h_ago) / self.price_24h_ago) * 100
            change_24h = current_price - self.price_24h_ago

            if change_24h > 0:
                color = "green"
                change_24h_text = f"↑ {change_24h:.2f}€ (↑ {percentage_change:.2f}%)"
            else:
                color = "red"
                change_24h_text = f"↓ {abs(change_24h):.2f}€ (↓ {abs(percentage_change):.2f}%)"

            self.current_price_label.configure(text=f"Prix du Bitcoin : {current_price:.2f}€", text_color=color)
            self.change_label.configure(text=f"Changement depuis 24h : {change_24h_text}", text_color=color)
            self.percentage_label.configure(text=f"Variation depuis le lancement : {percentage_change:.2f}%", text_color=color)
            self.previous_price = current_price
        else:
            self.current_price_label.configure(text="", text_color=color)
            self.change_label.configure(text="Erreur lors de la récupération du prix", text_color=color)
            self.percentage_label.configure(text="", text_color=color)

    def start_updating(self):
        def update_loop():
            while True:
                self.update_price()
                time.sleep(TIME_TO_SLEEP)

        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Utiliser le mode d'apparence sombre
    app = BitcoinPriceApp()
    app.mainloop()