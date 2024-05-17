import requests
import time
import customtkinter as ctk
import threading
from settings import *

class BitcoinPriceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        print("Initialisation de l'application...")
        self.title("")
        self.iconbitmap(EMPTY_ICON)
        self.geometry("450x100")
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')  # Centrer la fenêtre
        self.percentage_label = ctk.CTkLabel(self, font=PERCENTAGE_FONT)
        self.percentage_label.pack(pady=(10, 10))

        self.label = ctk.CTkLabel(self, text="Prix du Bitcoin : Récupération en cours...", font=CUSTOM_FONT)
        self.label.pack(pady=(0, 10))

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
        color = "white"
        if current_price is not None:
            if self.initial_price is None:
                self.initial_price = current_price

            price_diff = current_price - self.initial_price
            percentage_change = ((current_price - self.initial_price) / self.initial_price) * 100

            if price_diff > 0:
                color = "green"
                label_text = f"(↑ {price_diff}€ depuis le lancement)"
                percentage_text = f"↑ {percentage_change:.2f}%"
            elif price_diff < 0:
                color = "red"
                label_text = f"(↓ {-price_diff}€ depuis le lancement)"
                percentage_text = f"↓ {percentage_change:.2f}%"
            else:
                label_text = "(→ 0€ depuis le lancement)"
                percentage_text = "→ 0%"

            self.label.configure(text=f"Prix du Bitcoin : {current_price}€ {label_text}", text_color=color)
            self.percentage_label.configure(text=percentage_text, text_color=color)
            self.previous_price = current_price

    def start_updating(self):
        def update_loop():
            while True:
                self.update_price()
                time.sleep(TIME_TO_SLEEP)

        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Utiliser le mode d'apparence clair
    app = BitcoinPriceApp()
    app.mainloop()
