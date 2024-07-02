import csv
import numpy as np
import sys

# Check if the file path is provided as an argument
if len(sys.argv) < 2:
    print("Please provide the file path as an argument.")
    sys.exit(1)


# Get the file path from the command line argument
file_path = sys.argv[1]


# Create lists to store the statistics
all_transactions = []
all_gas_used = []
all_time_consumption = []


# Read the CSV file
with open(file_path, 'r') as file:
    reader = csv.reader(file, delimiter='|')
    for row in reader:
        height = int(row[0])
        gas_used = int(row[1])
        transactions = int(row[2])
        time_consumption = int(row[3])

        # Ignore rows where transactions or gas used are equal to 0
        if transactions == 0 or gas_used == 0:
            continue
        
        all_transactions.append(transactions)
        all_gas_used.append(gas_used)
        all_time_consumption.append(time_consumption)


# Convert the lists to numpy arrays
all_transactions = np.array(all_transactions)
all_gas_used = np.array(all_gas_used)
all_time_consumption = np.array(all_time_consumption)

# Calculate the statistics for all heights

avg_transactions = np.mean(all_transactions)
median_transactions = np.median(all_transactions)
p90_transactions = np.percentile(all_transactions, 90)
p99_transactions = np.percentile(all_transactions, 99)

avg_gas_used = np.mean(all_gas_used)
median_gas_used = np.median(all_gas_used)
p90_gas_used = np.percentile(all_gas_used, 90)
p99_gas_used = np.percentile(all_gas_used, 99)

avg_time_consumption = np.mean(all_time_consumption)
median_time_consumption = np.median(all_time_consumption)
p90_time_consumption = np.percentile(all_time_consumption, 90)
p99_time_consumption = np.percentile(all_time_consumption, 99)

# Print the statistics for all heights
print("Statistics for all heights:")
print(f"\nTransactions\n\tAvg:\t{avg_transactions}\n\tMedian:\t{median_transactions}\n\tP90:\t{p90_transactions}\n\tP99:\t{p99_transactions}")
print(f"\nGas Used\n\tAvg:\t{avg_gas_used}\n\tMedian:\t{median_gas_used}\n\tP90:\t{p90_gas_used}\n\tP99:\t{p99_gas_used}")
print(f"\nTime Consumption (ms)\n\tAvg:\t{avg_time_consumption}\n\tMedian:\t{median_time_consumption}\n\tP90:\t{p90_time_consumption}\n\tP99:\t{p99_time_consumption}")
