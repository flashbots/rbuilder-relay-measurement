import requests
import json
import os
import argparse

def fetch_slot_data(base_url, slot):
    url = f"{base_url}/relay/v1/data/bidtraces/builder_blocks_received"
    params = {
        'slot': slot
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Fetch the winner bid
    winner_url = f"{base_url}/relay/v1/data/bidtraces/proposer_payload_delivered"
    winner_response = requests.get(winner_url, params=params)
    winner_data = winner_response.json()
    if not winner_data:
        return data, {}
    # Fetch the winner's full data
    winner_full_data_url = f"{base_url}/relay/v1/data/bidtraces/builder_blocks_received"
    winner_full_data_params = {
        'slot': slot,
        'builder_pubkey': winner_data[0]['builder_pubkey'],
        'block_hash': winner_data[0]['block_hash']
    }
    winner_full_data_response = requests.get(winner_full_data_url, params=winner_full_data_params)
    winner_full_data = winner_full_data_response.json()
    return data, winner_full_data

def store_slot_data(slot, data, winner_full_data):
    os.makedirs('slots_data', exist_ok=True)
    with open(os.path.join('slots_data', f'{slot}.json'), 'w') as f:
        json.dump(data, f)
    with open(os.path.join('slots_data', f'{slot}_bid_winner.json'), 'w') as f:
        json.dump(winner_full_data, f)

def main():
    parser = argparse.ArgumentParser(description='Fetch slot data.')
    parser.add_argument('slot', type=int, help='Slot number')
    parser.add_argument('--base_url', type=str, default='https://relay-analytics.ultrasound.money', help='Base URL')
    args = parser.parse_args()

    data, winner_full_data = fetch_slot_data(args.base_url, args.slot)
    store_slot_data(args.slot, data, winner_full_data)

if __name__ == "__main__":
    main()