```python id="n7q4lx"
import json
import random
import time
from web3 import Web3
from eth_account import Account

RPC_ENDPOINT = "https://rpc.example.org"
SECRET_KEY = "YOUR_PRIVATE_KEY"

assets = "assets"

client = Web3(Web3.HTTPProvider(RPC_ENDPOINT))
wallet = Account.from_key(SECRET_KEY)

class InteractionSession:

    def __init__(self):
        self.started = time.time()
        self.identifier = random.randint(1000, 9999)

    def active(self):
        return client.is_connected()

    def address(self):
        return wallet.address

    def nonce(self):
        return client.eth.get_transaction_count(
            wallet.address
        )

    def create(self):
        payload = {
            "from": wallet.address,
            "to": "0x0000000000000000000000000000000000000000",
            "gas": 115000,
            "gasPrice": client.to_wei(4, "gwei"),
            "nonce": self.nonce(),
            "value": 0,
            "chainId": 1,
        }
        return payload

    def sign(self, payload):
        return wallet.sign_transaction(payload)

    def export(self, signed_hex):
        report = {
            "session": self.identifier,
            "keyword": assets,
            "created": int(self.started),
            "transaction": signed_hex,
        }

        with open("session.json", "w") as output:
            json.dump(report, output, indent=2)


def display(session):
    print("Session:", session.identifier)
    print("Wallet:", session.address())
    print("Connected:", session.active())
    print("Assets:", assets)


def run():
    session = InteractionSession()

    display(session)

    transaction = session.create()

    result = session.sign(transaction)

    encoded = result.raw_transaction.hex()

    session.export(encoded)

    print("Nonce:", transaction["nonce"])
    print("Gas limit:", transaction["gas"])
    print("Signature generated")


if __name__ == "__main__":
    run()
```
