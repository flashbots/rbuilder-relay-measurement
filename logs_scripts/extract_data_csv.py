import re
import csv
import sys
import os

# Updated pattern to match the correct order of fields
pattern = re.compile(r'"block":(\d+).*?"fill_time_ms":"(\d+)".*?"finalize_time_ms":"(\d+)".*?"gas":(\d+).*?"txs":(\d+)', re.DOTALL)

def process_log_file(file_path):
    data = []
    matches_found = 0
    with open(file_path, 'r') as file:
        content = file.read()
        for match in pattern.finditer(content):
            matches_found += 1
            block = match.group(1)
            fill_time = int(match.group(2))
            finalize_time = int(match.group(3))
            gas = match.group(4)
            txs = match.group(5)
            time_consumption = fill_time + finalize_time
            data.append([block, gas, txs, time_consumption])
    print(f"Finished processing. Total matches found: {matches_found}")
    return data

def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='|')
       #writer.writerow(['block', 'gas', 'txs', 'time_consumption'])
        writer.writerows(data)
    print(f"Wrote {len(data)} rows to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_data_csv.py <path_to_log_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    
    if not os.path.isfile(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        sys.exit(1)

    output_file = 'output.csv'
    
    print(f"Processing file: {input_file}")
    extracted_data = process_log_file(input_file)
    
    if not extracted_data:
        print("No matching data found in the log file. The output file will be empty.")
    else:
        write_to_csv(extracted_data, output_file)
        print(f"Data has been extracted from '{input_file}' and written to '{output_file}'")

    # Print the first few rows of extracted data for verification
    print("\nFirst few rows of extracted data:")
    for row in extracted_data[:5]:
        print("|".join(map(str, row)))
