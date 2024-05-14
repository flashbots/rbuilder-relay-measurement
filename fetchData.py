import os
import requests
import sys
import json
import datetime
import json

DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def fetch_data(builder_pubkey, block_number=None):
    filename = f"{builder_pubkey[:6]}_{block_number}"
    filepath = os.path.join(DATA_FOLDER, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            data = json.load(file)
    else:
        url = "https://relay.ultrasound.money/relay/v1/data/bidtraces/builder_blocks_received"
        params = {
            'builder_pubkey': builder_pubkey,
            'block_number': block_number
        }
        response = requests.get(url, params=params)
        data = response.json()

        with open(filepath, "w") as file:
            json.dump(data, file)

    return data
    
def compare_data(file_path, fetched_data):
    with open(file_path, "r") as file:
        file_data = file.readlines()

    file_data = [json.loads(line.strip()) for line in file_data]

    for i, item in enumerate(file_data):
        fetched_item = fetched_data[i]
        timestamp_file = item.get("timestamp")
        timestamp_fetched = fetched_item.get("timestamp_ms")
        gas_file = item.get("spans")[0].get("gas")
        gas_fetched = fetched_item.get("gas_used")
        num_transactions_file = item.get("spans")[0].get("txs")
        num_transactions_fetched = fetched_item.get("num_tx")
        
        
        if timestamp_file and timestamp_fetched:
            timestamp_file_obj = datetime.datetime.strptime(timestamp_file,'%Y-%m-%dT%H:%M:%S.%fZ')
            timestamp_file_ms = timestamp_file_obj.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000
            timestamp_diff = int(timestamp_fetched) - int(timestamp_file_ms)
            print(f"Timestamp difference for item {i+1}: {timestamp_diff} milliseconds")
        
        if gas_file and gas_fetched:
            if int(gas_file) != int(gas_fetched):
                print(f"Gas used for item {i+1} is different")
        

        if num_transactions_file and num_transactions_fetched:
            if int(num_transactions_file) != int(num_transactions_fetched):
                print(f"Number of transactions for item {i+1} is different , {num_transactions_file} and {num_transactions_fetched}")

        if item.get("spans")[1].get("optimistic") != fetched_item.get("optimistic_submission"):
            print(f"item {i+1} have different optimistic fields values set")
            

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <builder_pubkey> <block_numbery> <rbuilder_logs>")
        sys.exit(1)
    
    builder_pubkey = sys.argv[1]
    block_number = sys.argv[2]
    file_path = sys.argv[3]

    data = fetch_data(builder_pubkey, block_number)
    data.reverse()

    # Convert timestamp_ms to human-readable form
    """
    for item in data:
        timestamp_ms = item.get("timestamp_ms")
        if timestamp_ms:
            timestamp = datetime.datetime.utcfromtimestamp(int(timestamp_ms) / 1000).replace(microsecond=int(timestamp_ms) % 1000 * 1000)
            #item["timestamp_ms"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
    """        
    #print(json.dumps(data, indent=4))
    compare_data(file_path, data)

