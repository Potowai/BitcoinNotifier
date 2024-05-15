import json
import os
import requests
import time
from customtkinter import CTk, CTkLabel
from playsound import playsound

# Chemin vers le fichier JSON
JSON_FILE = "previous_price.json"

# Fonction pour obtenir le prix actuel du Bitcoin
def get_bitcoin_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur'
    response = requests.get(url)
    data = response.json()
    try:
        return data['bitcoin']['eur']
    except KeyError:
        print("Error occurred while fetching the price. Retrying...")
        time.sleep(5)
        return get_bitcoin_price()

# Fonction pour récupérer le prix précédent à partir du fichier JSON
def get_previous_price():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    else:
        return None

# Fonction pour enregistrer le prix actuel dans le fichier JSON
def save_current_price(price):
    with open(JSON_FILE, "w") as file:
        json.dump(price, file)
        print("Price saved successfully!")

# Fonction principale pour vérifier les changements de prix
def check_price_changes():
    previous_price = get_previous_price()
    if previous_price is None:
        previous_price = get_bitcoin_price()
        save_current_price(previous_price)
    
    while True:
        current_price = get_bitcoin_price()
        price_label.configure(text=f"Bitcoin price: {current_price}€")
        price_diff = current_price - previous_price
        
        if abs(price_diff) >= 1000:
            if price_diff > 0:
                print("Bitcoin gained 1000€!")
            else:
                print("Bitcoin lost 1000€!")
            playsound("path_to_your_wav_file.wav")  # Remplacez par le chemin de votre fichier .wav
            previous_price = current_price
            save_current_price(previous_price)
        
        time.sleep(10)  # Vérifier toutes les minutes

# Créer une fenêtre
window = CTk()

# Créer un widget Label pour afficher le prix
price_label = CTkLabel(window, text="Bitcoin price: Loading...")
price_label.pack()

window.after(0, check_price_changes)

# Démarrer la boucle principale de l'interface graphique
window.mainloop()

