import argparse
import subprocess
import json
import os

def compare_data(builder_pubkey, slot, base_url=None):
    data_file = os.path.join('slots_data', f'{slot}.json')
    winner_file = os.path.join('slots_data', f'{slot}_bid_winner.json')

    if not os.path.exists(data_file) or not os.path.exists(winner_file):
        command = ['python3', 'fetch_slot_data.py', str(slot)]
        if base_url:
            command.extend(['--base-url', base_url])
        subprocess.run(command)

    with open(data_file, 'r') as f:
        data = json.load(f)

    if not data:
        print(f"No submissions/bids found for slot {slot}")
        return
    
    with open(winner_file, 'r') as f:
        winner_full_data = json.load(f)
        if winner_full_data:
            winner_full_data = winner_full_data[0]
        else:
            print("No bids won in this slot from this relay")
            return

    if winner_full_data['builder_pubkey'] == builder_pubkey:
        print("Your bid won in this slot!")
        return

    filtered_data = [item for item in data if item['builder_pubkey'] == builder_pubkey]
    if not filtered_data:
        print("Your builder pubkey did not submit any bid for this slot")
        return
    
    print(f"Comparing builder's submissions against the slot's winner")
    for i, item in enumerate(filtered_data):
        print(f"Bid {i+1}:")
        print(f"    Value difference: {int(winner_full_data['value']) - int(item['value'])}")
        print(f"    Gas used difference: {int(winner_full_data['gas_used']) - int(item['gas_used'])}")
        print(f"    Num_tx difference: {int(winner_full_data['num_tx']) - int(item['num_tx'])}")
        print(f"    Timestamp_ms difference: {int(winner_full_data['timestamp_ms']) - int(item['timestamp_ms'])}")

def main():
    parser = argparse.ArgumentParser(description='Compare builder data with winner data.')
    parser.add_argument('builder_pubkey', type=str, help='Builder public key')
    parser.add_argument('slot', type=int, help='Slot number')
    parser.add_argument('--base_url', type=str, help='Base URL')
    args = parser.parse_args()

    compare_data(args.builder_pubkey, args.slot, args.base_url)

if __name__ == "__main__":
    main()
