# rbuilder-relay-measurement
A script to pull data for a specific block number and builder public key from the relay and compare them against those from the builder logs

# Example for compare_builder_relay.py
```python compare_builder_relay.py 0xa1aa1ad4f2ad89f3cd2da667259022763ce7d22f75582fc824cd6cc8c56a89edb6a922e64ab95666f4bdeb2c309052ef 19867351 builder.json```

# Preparations
1. fetch the builder logs for the specific relay and preferably filter for a specific block number (see builder.json), for example
``` 
journalctl --since "1 hour ago" -u rbuilder -o cat | grep  "\"relay\":\"ultrasound\"" | grep "\"message\":\"Block submitted to the relay successfully\"" > builder.json  
```
2. run the script with the builders pubkey, block number and the builder.json that you extracted from the previous step. 

# Example for compare_winenr.py
```python compare_winner.py 0xa1aa1ad4f2ad89f3cd2da667259022763ce7d22f75582fc824cd6cc8c56a89edb6a922e64ab95666f4bdeb2c309052ef```

# Example for analyse_slot.py
```python3 analyse_slot.py 0xa1aa1ad4f2ad89f3cd2da667259022763ce7d22f75582fc824cd6cc8c56a89edb6a922e64ab95666f4bdeb2c309052ef 9085513```

You can also optionally pass a base url to specify which relay you want to fetch the data from.
This script will internal call the ```fetch_slot_data.py```. It will fetch the data and put them into the folder ```slot_data``` to be later used in the analysis.
