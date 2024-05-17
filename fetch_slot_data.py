import requests
import json
import os
import argparse
import consts


def fetch_winner_data(base_url, slot):
    # Check if the bid winner data already exists
    winner_data_path = os.path.join(consts.SLOTS_DATA_PATH, f"{slot}_bid_winner.json")
    if os.path.exists(winner_data_path):
        with open(winner_data_path, "r") as f:
            winner_full_data = json.load(f)
        return winner_full_data

    # Fetch the winner bid
    winner_url = f"{base_url}/relay/v1/data/bidtraces/proposer_payload_delivered"
    params = {"slot": slot}
    winner_response = requests.get(winner_url, params=params)
    winner_data = winner_response.json()
    if not winner_data:
        return {}

    # Fetch the winner's full data
    winner_full_data_url = f"{base_url}/relay/v1/data/bidtraces/builder_blocks_received"
    winner_full_data_params = {
        "slot": slot,
        "builder_pubkey": winner_data[0]["builder_pubkey"],
        "block_hash": winner_data[0]["block_hash"],
    }
    winner_full_data_response = requests.get(
        winner_full_data_url, params=winner_full_data_params
    )
    winner_full_data = winner_full_data_response.json()

    # Store the fetched winner data
    with open(winner_data_path, "w") as f:
        json.dump(winner_full_data, f)

    return winner_full_data


def fetch_slot_data(base_url, slot):

    # Check if the slot data already exists
    slot_data_path = os.path.join(consts.SLOTS_DATA_PATH, f"{slot}.json")
    if os.path.exists(slot_data_path):
        with open(slot_data_path, "r") as f:
            data = json.load(f)
        return data

    # Fetch the slot data from the API
    url = f"{base_url}/relay/v1/data/bidtraces/builder_blocks_received"
    params = {"slot": slot}
    response = requests.get(url, params=params)
    data = response.json()

    # Store the fetched data
    with open(slot_data_path, "w") as f:
        json.dump(data, f)

    return data


def fetch(slot, base_url=consts.URL_ULTRASOUND):
    data = fetch_slot_data(base_url, slot)
    winner_full_data = fetch_winner_data(base_url, slot)
    return data, winner_full_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch slot data.")
    parser.add_argument("slot", type=int, help="Slot number")
    parser.add_argument(
        "--base_url", type=str, default=consts.URL_ULTRASOUND, help="Base URL"
    )
    args = parser.parse_args()

    fetch(args.slot, args.base_url)
