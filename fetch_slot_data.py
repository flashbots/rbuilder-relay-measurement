import requests
import json
import os
import argparse
import consts



def fetch_winner_data(base_url, slot, params):
    # Fetch the winner bid
    winner_url = f"{base_url}/relay/v1/data/bidtraces/proposer_payload_delivered"
    winner_response = requests.get(winner_url, params=params)
    winner_data = winner_response.json()
    if not winner_data:
        return {}
    # Fetch the winner's full data
    winner_full_data_url = f"{base_url}/relay/v1/data/bidtraces/builder_blocks_received"
    winner_full_data_params = {
        'slot': slot,
        'builder_pubkey': winner_data[0]['builder_pubkey'],
        'block_hash': winner_data[0]['block_hash']
    }
    winner_full_data_response = requests.get(winner_full_data_url, params=winner_full_data_params)
    winner_full_data = winner_full_data_response.json()
    return winner_full_data

def fetch_slot_data(base_url, slot):
    url = f"{base_url}/relay/v1/data/bidtraces/builder_blocks_received"
    params = {
        'slot': slot
    }
    response = requests.get(url, params=params)
    data = response.json()

    winner_full_data = fetch_winner_data(base_url, slot, params)

    return data, winner_full_data


def store_slot_data(slot, data, winner_full_data):
    os.makedirs(consts.SLOTS_DATA_PATH, exist_ok=True)
    with open(os.path.join(consts.SLOTS_DATA_PATH, f'{slot}.json'), 'w') as f:
        json.dump(data, f)
    with open(os.path.join(consts.SLOTS_DATA_PATH, f'{slot}_bid_winner.json'), 'w') as f:
        json.dump(winner_full_data, f)

def main(slot, base_url=consts.URL_ULTRASOUND):
    data, winner_full_data = fetch_slot_data(base_url, slot)
    store_slot_data(slot, data, winner_full_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch slot data.')
    parser.add_argument('slot', type=int, help='Slot number')
    parser.add_argument('--base_url', type=str, default=consts.URL_ULTRASOUND, help='Base URL')
    args = parser.parse_args()

    main(args.slot, args.base_url)