import argparse
import requests
import time

def fetch_winning_slots(builder_pubkey, limit=None):
    url = 'https://relay-analytics.ultrasound.money/relay/v1/data/bidtraces/proposer_payload_delivered'
    params = {
        'builder_pubkey': builder_pubkey,
        'limit': limit
    }
    response = requests.get(url, params=params)
    data = response.json()
    slots = [item['slot'] for item in data]
    return slots

def main():
    parser = argparse.ArgumentParser(description='Fetch winning slots by builder pubkey.')
    parser.add_argument('builder_pubkey', type=str, help='Builder public key')
    parser.add_argument('--limit', type=int, default=100, help='Limit for number of iterations')
    args = parser.parse_args()

    won_slots = fetch_winning_slots(args.builder_pubkey, args.limit)
    print(f"Won slots: {won_slots}")

if __name__ == "__main__":
    main()
