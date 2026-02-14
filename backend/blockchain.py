from web3 import Web3
import json
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
CHAIN_ID = int(os.getenv("CHAIN_ID"))

# Connect to Sepolia
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    raise Exception("Failed to connect to Sepolia RPC")

# Load ABI
with open("abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)

account = w3.eth.account.from_key(PRIVATE_KEY)

def store_hash(data):

    # Convert data to JSON string
    data_string = json.dumps(data)

    # Generate SHA256 hash
    data_hash = hashlib.sha256(data_string.encode()).hexdigest()

    # Get nonce
    nonce = w3.eth.get_transaction_count(account.address)

    # Build transaction
    transaction = contract.functions.storeHash(data_hash).build_transaction({
        "chainId": CHAIN_ID,
        "from": account.address,
        "nonce": nonce,
        "gas": 200000,
        "gasPrice": w3.eth.gas_price
    })

    # Sign transaction
    signed_tx = account.sign_transaction(transaction)

    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return {
        "data_hash": data_hash,
        "transaction_hash": tx_hash.hex()
    }
