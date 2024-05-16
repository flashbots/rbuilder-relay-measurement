import requests
import datetime

# helpers
slot_time = lambda slot: (slot * 12) + 1606824023

slot_time_str = lambda slot: datetime.datetime.utcfromtimestamp(
    slot_time(slot)
).strftime("%Y-%m-%d %H:%M:%S")


def get_latest_slot():
    url = "https://beaconcha.in/latestState"
    c = requests.get(url).json()
    return c["lastProposedSlot"]
