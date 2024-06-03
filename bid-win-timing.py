import utils
import consts
import fetch_slot_data

"""
Check timing of winning bids

Example usage (saving output into file):

    python3 -u bid-win-timing.py | tee wins.txt

"""

NUM_SLOTS = 100
START_SLOT = 0  # latest

start_slot = START_SLOT or utils.get_latest_slot()

overall_data = []


def check_winning_submission(slot):
    print(f"\nfetching winning bid data for slot {slot} ...")
    for relay, url in consts.RELAYS.items():
        try:
            data = fetch_slot_data.fetch_winner_data(url, slot)
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")
            continue
        if data:
            break
    if not data:
        return

    bid_timestamp_ms = int(data[0]["timestamp_ms"])
    bid_block_hash = data[0]["block_hash"]
    slot_start_timestamp_ms = utils.slot_time(slot) * 1000
    t_ms = bid_timestamp_ms - slot_start_timestamp_ms
    overall_data.append(
        (str(slot), str(bid_timestamp_ms), str(t_ms), bid_block_hash, relay)
    )
    print(f"- Winning bid {bid_block_hash} t = {t_ms} ms (via {relay})")


for i in range(NUM_SLOTS):
    check_winning_submission(start_slot - i)

for d in overall_data:
    print("\t".join(d))
