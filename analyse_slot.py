import argparse
import subprocess
import json
import os
import consts
import fetch_slot_data

def compare_data(builder_pubkey, slot, base_url=None):
    if base_url is None:
        data, winner_full_data = fetch_slot_data.fetch(slot)
    else:
        data, winner_full_data = fetch_slot_data.fetch(slot, base_url)
    
    if not data:
        print(f"No submissions/bids found for slot {slot}")
        return
    
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
