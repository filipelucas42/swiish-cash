from web3 import Web3
from eth_account import Account
import secrets

# Connect to Avalanche C-Chain
avalanche_url = "https://api.avax.network/ext/bc/C/rpc"
w3 = Web3(Web3.HTTPProvider(avalanche_url))

def create_wallet():
    # Generate a private key
    private_key = "0x" + secrets.token_hex(32)
    
    # Create account from private key
    account = Account.from_key(private_key)
    print("address " + account.address)
    print("private " + private_key)
    
    return {
        "address": account.address,
        "private_key": private_key
    }

# Example usage
def main():
    wallet = create_wallet()
    print(f"New Avalanche C-Chain Address: {wallet['address']}")
    print(f"Private Key: {wallet['private_key']}")
    
    # Verify connection
    print(f"Connected to Avalanche: {w3.is_connected()}")
    
if __name__ == "__main__":
    main()