import time
import telebot
import web3
from web3 import Web3

# Replace 'YOUR_BOT_TOKEN' with your token generated from BotFather
bot = telebot.TeleBot("YOUR_BOT_TOKEN")

# Setup the variables for the private key and the public key of the compromised wallet and the safe receiver address
privk_compromised = ""
pubk_compromised = ""
safe_receiver = ""

# Replace 'YOUR_API_KEY' with your API key released from Infura, change the provider accordingly to the network where you want to run this bot
web3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/YOUR_API_KEY'))

# Replace 'YOUR_CONTRACT_ADDRESS' with the actual address of the token smart contract that you want to transfer out from the compromised wallet
contract_address = Web3.to_checksum_address('YOUR_CONTRACT_ADDRESS')

# Define the ABI of the token contract
# You need to replace this with the ABI of the specific token contract you're interacting with
token_abi_symbol = [
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

# Instantiate the contract object
contract = web3.eth.contract(address=contract_address, abi=token_abi_symbol)

# Call the symbol function of the token contract
token_symbol = contract.functions.symbol().call()


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, """Welcome to the Crypto Rescue Bot! \U0001F916

/test - Check message containing the private and public key of the compromised wallet, the safe receiver address and the exact token to rescue

/rescue - Check if a specific token is inside the compromised wallet and trigger the raw tx to move the funds towards a safe wallet""")


@bot.message_handler(commands=["test"])
def test(message):
    bot.send_message(message.chat.id, "Compromised private key: " + privk_compromised)
    bot.send_message(message.chat.id, "Compromised public key: " + pubk_compromised)
    bot.send_message(message.chat.id, "Safe receiver: " + safe_receiver)
    bot.send_message(message.chat.id, "Token to rescue: " + token_symbol)


@bot.message_handler(commands=["rescue"])
def rescue(message):
    bot.send_message(message.chat.id, "Start rescue...")

    # Define the token contract ABI
    token_abi_balance = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        }
    ]

    # Create the contract object
    token_contract = web3.eth.contract(address=contract_address, abi=token_abi_balance)

    # Define the interval for checking the balance (in seconds)
    check_interval = 5

    while True:
        # Get the balance of the token for the wallet address
        balance = token_contract.functions.balanceOf(pubk_compromised).call()

        bot.send_message(message.chat.id, "Balance of " + token_symbol + " is still 0. Re-checking...")

        # Check if balance is greater than zero
        if balance > 0:
            bot.send_message(message.chat.id, token_symbol + " received! Starting the recovery tx...")

            try:
                tx_hash = send_transaction(privk_compromised, safe_receiver, balance)
                bot.send_message(message.chat.id, f"Transaction sent successfully! Transaction Hash: {tx_hash.hex()}")
            except Exception as e:
                bot.send_message(message.chat.id, f"Error occurred while sending transaction: {str(e)}")

            break

        # Wait for the specified interval before checking again
        time.sleep(check_interval)


def send_transaction(private_key, receiver_address, amount):
    wallet_address = Web3.to_checksum_address(pubk_compromised)

    # Token contract details
    token_abi_transfer = [
        {
            "constant": False,
            "inputs": [
                {"name": "_to", "type": "address"},
                {"name": "_value", "type": "uint256"}
            ],
            "name": "transfer",
            "outputs": [{"name": "", "type": "bool"}],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]

    # Define recipient address and amount
    recipient_address = receiver_address
    amount = amount  # Amount of tokens to transfer

    # Create contract object
    token_contract = web3.eth.contract(address=contract_address, abi=token_abi_transfer)

    # Encode function call
    data = token_contract.encodeABI('transfer', [recipient_address, amount])

    # Build transaction
    nonce = web3.eth.get_transaction_count(wallet_address)
    gas_price = web3.eth.gas_price
    gas_limit = 100000  # Adjust as needed based on token contract specifics

    transaction = {
        'nonce': nonce,
        'to': contract_address,
        'value': 0,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'data': data,
        'chainId': 11155111  # Sepolia, if you want to run this script on other networks make sure to change the chainId parameter
    }

    # Sign transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

    # Send raw transaction
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    return tx_hash

if __name__ == "__main__":
    print("Ok \U0001F680")
    bot.polling()
