import requests
import time
import random
from faker import Faker

# --- CONFIGURATION ---
# After you deploy your backend, replace this with your live Render URL
API_ENDPOINT = "http://127.0.0.1:8000/api/transactions/"
TRANSACTIONS_PER_MINUTE = 20

# Initialize the fake data generator
fake = Faker()

def generate_transaction():
    """Creates a single, random mock transaction."""
    
    # 80% chance of a "normal" transaction, 20% chance of a "risky" one
    if random.random() < 0.8:
        # Generate a compliant-looking transaction
        trans_type = "WIRE"
        amount = round(random.uniform(500.0, 15000.0), 2)
        client = fake.company()
    else:
        # Generate a risky-looking transaction
        trans_type = "CRYPTO"
        amount = round(random.uniform(50000.0, 750000.0), 2)
        client = f"{fake.word().capitalize()} Capital Ventures"

    return {
        "transaction_id_str": f"TXN-SIM-{fake.uuid4()[:8]}",
        "transaction_type": trans_type,
        "amount": f"{amount:.2f}",
        "currency": "USD",
        "client_name": client,
        "source_account": f"ACC-{fake.msisdn()}",
        "destination_account": f"ACC-{fake.msisdn()}"
    }

def run_simulator():
    """Main loop to continuously generate and post transactions."""
    print("--- Starting Real-Time Transaction Stream Simulator ---")
    print(f"Targeting API Endpoint: {API_ENDPOINT}")
    print(f"Generating approximately {TRANSACTIONS_PER_MINUTE} transactions per minute.")
    
    sleep_interval = 60 / TRANSACTIONS_PER_MINUTE
    
    while True:
        try:
            transaction_data = generate_transaction()
            print(f"Generated {transaction_data['transaction_type']} transaction for {transaction_data['amount']}...")
            
            response = requests.post(API_ENDPOINT, json=transaction_data)
            
            if response.status_code == 201:
                print(f"  -> Successfully sent transaction {transaction_data['transaction_id_str']} to QERCAS.")
            else:
                print(f"  -> ERROR: Failed to send transaction. Status: {response.status_code}, Response: {response.text}")

            time.sleep(sleep_interval)
            
        except requests.exceptions.ConnectionError:
            print("\nERROR: Connection to the API endpoint failed. Is the Django server running?")
            print("Retrying in 10 seconds...")
            time.sleep(10)
        except KeyboardInterrupt:
            print("\n--- Simulator stopped by user. ---")
            break

if __name__ == "__main__":
    run_simulator()
