import string
import requests

num_slots = 1000  # number of slots to work back from start slot (if earliest_slot is not set or reached)
start_slot = 0  # by default starts at latest slot
earliest_slot = 0  # earliest slot to check, stop when arrived there
outfile = "extradata.tsv"

f = open(outfile, "w")


def get_latest_slot():
    url = "https://beaconcha.in/api/v1/slot/latest"
    c = requests.get(url).json()
    return c["data"]["slot"]


def get_extradata(slot):
    url = f"https://beaconcha.in/api/v1/slot/{slot}"
    response = requests.get(url).json()
    if not response:
        return "error: no response"
    elif not "data" in response:
        return "error: response without data: {response}"
    elif not response["data"]:
        return "error: response with empty data: {response}"
    elif "exec_extra_data" not in response["data"]:
        return "error: response without extra_data: {response}"
    else:
        extra_data_hex = response["data"]["exec_extra_data"]
        if not extra_data_hex:
            return ""

        extra_data_bytes = bytes.fromhex(extra_data_hex[2:])
        extra_data = extra_data_bytes.decode("utf-8", errors="ignore")
        if not extra_data:
            return ""

        # Remove funky characters
        allowed = string.digits + string.ascii_letters + string.punctuation + " "
        return "".join(filter(lambda x: x in allowed, extra_data))


slot = start_slot
if slot == 0:
    slot = get_latest_slot()

print("slot    \t extra_data")
f.write("slot\textra_data\n")
slot += 1
for i in range(num_slots):
    slot -= 1
    if slot < earliest_slot:
        break
    extra_data = get_extradata(slot)
    print(f"{slot} \t {extra_data}")
    f.write(f"{slot} \t {extra_data}\n")
    f.flush()
