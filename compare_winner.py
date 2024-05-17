import requests
import argparse


def fetch_data(builder_pubkey, limit):
    url = "https://relay-analytics.ultrasound.money/relay/v1/data/bidtraces/builder_blocks_received"
    params = {"builder_pubkey": builder_pubkey, "limit": limit}
    response = requests.get(url, params=params)
    data = response.json()
    slots_data = {}
    for item in data:
        if item["slot"] in slots_data:
            slots_data[item["slot"]].append(item)
        else:
            slots_data[item["slot"]] = [item]
    return slots_data


def fetch_and_compare(slot, builder_data_list):
    url = "https://relay-analytics.ultrasound.money/relay/v1/data/bidtraces/proposer_payload_delivered"
    params = {"slot": slot}
    response = requests.get(url, params=params)
    data = response.json()
    if data:
        url = "https://relay-analytics.ultrasound.money/relay/v1/data/bidtraces/builder_blocks_received"
        params = {
            "builder_pubkey": data[0]["builder_pubkey"],
            "slot": slot,
            "block_hash": data[0]["block_hash"],
        }
        response = requests.get(url, params=params)
        winner_data = response.json()

        if not winner_data:
            print(f"No bid won slot {slot} from this relay.")
            return

        winner_data = winner_data[0]

        if not winner_data:
            print(f"No bid won slot {slot} from this relay.")
            return

        print(f"Comparing for slot {slot}")
        for i, builder_data in enumerate(builder_data_list):
            print(f"Comparing builder's {i+1} submission against the slot's winner")
            if builder_data["builder_pubkey"] == winner_data["builder_pubkey"]:
                print("Your builder pubkey bid won this slot!")
                break
            print(
                f"Value difference: {int(winner_data['value']) - int(builder_data['value'])}"
            )
            print(
                f"Gas used difference: {int(winner_data['gas_used']) - int(builder_data['gas_used'])}"
            )
            print(
                f"Num_tx difference: {int(winner_data['num_tx']) - int(builder_data['num_tx'])}"
            )
            print(
                f"Timestamp difference: {int(winner_data['timestamp_ms']) - int(builder_data['timestamp_ms'])}"
            )
            print()  # Add an empty line for better readability


def main():
    parser = argparse.ArgumentParser(description="Fetch and compare data.")
    parser.add_argument("builder_pubkey", type=str, help="Builder public key")
    parser.add_argument(
        "--limit",
        type=int,
        default=500,
        help="Limit for the number of records to fetch",
    )
    args = parser.parse_args()

    slots_data = fetch_data(args.builder_pubkey, args.limit)
    for slot, builder_data_list in slots_data.items():
        fetch_and_compare(slot, builder_data_list)


if __name__ == "__main__":
    main()
