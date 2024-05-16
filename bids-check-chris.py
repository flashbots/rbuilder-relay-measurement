"""
Check bids submitted by Flashbots builders for the last N slots

Example output: https://gist.github.com/metachris/71c1c9a4b0f23713be283ad91f33a534
"""

import utils
import consts
import fetch_slot_data
from collections import defaultdict

num_slots = 50

relay = consts.URL_ULTRASOUND
# relay = consts.URL_FLASHBOTS

start_slot = utils.get_latest_slot()
# start_slot = 9088031

print(
    f"Checking bids for {num_slots} slots ({start_slot-num_slots} to {start_slot}) at {relay} ..."
)

flashbots_builders_bids_submitted_overall = defaultdict(int)


def check_flashbots_submissions(slot):
    print(f"\nfetching data for slot {slot} ...")
    data, winner = fetch_slot_data.fetch_slot_data(relay, slot)

    flashbots_builders_bids_submitted = defaultdict(int)

    for bid in data:
        for builder_type, builders in consts.FLASHBOTS_BUILDERS.items():
            key = builder_type[:3] + " " + bid["builder_pubkey"]
            if bid["builder_pubkey"] in builders:
                flashbots_builders_bids_submitted[key] += 1
                flashbots_builders_bids_submitted_overall[key] += 1

    for builder, count in flashbots_builders_bids_submitted.items():
        print(f"- {builder} submitted {count} bids")


for i in range(num_slots):
    check_flashbots_submissions(start_slot - i)

print()
print("----------------------")
print()
print(
    f"Overall bids for {num_slots} slots ({start_slot-num_slots} to {start_slot}) at {relay}:"
)
items_sorted = sorted(
    flashbots_builders_bids_submitted_overall.items(), key=lambda x: x[0], reverse=False
)
for builder, count in items_sorted:
    print(f"- {builder} submitted {count} bids")
