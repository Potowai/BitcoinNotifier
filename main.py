import requests
import time
from playsound import playsound

# Function to get current Bitcoin price
def get_bitcoin_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur'
    response = requests.get(url)
    data = response.json()
    return data['bitcoin']['eur']

# Main function to check for price changes
def check_price_changes():
    previous_price = get_bitcoin_price()
    
    while True:
        playsound("80s synthé sound.wav")
        current_price = get_bitcoin_price()
        price_diff = current_price - previous_price
        
        if abs(price_diff) >= 1000:
            if price_diff > 0:
                print("Bitcoin gained 1000€!")
                playsound("instrumental notif sound.wav")
            else:
                print("Bitcoin lost 1000€!")
                playsound("broken glass sound.wav")  # Replace with path to your .wav file
            previous_price = current_price
        
        time.sleep(60)  # Check every minute

# Run the script
if __name__ == "__main__":
    playsound("80s synthé sound.wav")
    check_price_changes()
