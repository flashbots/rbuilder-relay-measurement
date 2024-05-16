import utils
import consts
import fetch_slot_data
from collections import defaultdict

num_slots = 5

latest_slot = utils.get_latest_slot()
epoch = latest_slot // 32
print(f"latest slot: {latest_slot}, epoch: {epoch}")


def check_flashbots_submissions(slot):
    print(f"fetching data for slot {slot} ...")
    data, winner = fetch_slot_data.fetch_slot_data(consts.URL_ULTRASOUND, slot)

    flashbots_builders_bids_submitted = defaultdict(int)

    for entry in data:
        if entry["builder_pubkey"] in consts.FLASHBOTS_BUILDERS_VANILLA:
            # print(f"vanilla: {entry['builder_pubkey']}")
            flashbots_builders_bids_submitted["van " + entry["builder_pubkey"]] += 1
        if entry["builder_pubkey"] in consts.FLASHBOTS_BUILDERS_TDX:
            # print(f"tdx: {entry['builder_pubkey']}")
            flashbots_builders_bids_submitted["tdx " + entry["builder_pubkey"]] += 1

    for builder, count in flashbots_builders_bids_submitted.items():
        print(f"- {builder} submitted {count} bids")


for i in range(num_slots):
    check_flashbots_submissions(latest_slot - i)
