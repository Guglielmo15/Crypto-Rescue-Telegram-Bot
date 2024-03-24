# Crypto-Rescue-Telegram-Bot

This is a Python-based Telegram bot that allows users to withdraw a specific token from a compromised wallet.

Let's assume that your private key has been stolen and the attacker requested a withdraw from the staking or from whatever other kind of locked vault, as soon as the tokens will be sent into the compromised wallet the attacker will have access to it, unless you're faster than him and send instantly those tokens to a safe address where you're still in control over the private key.

That's where this bot can help, let's see the process.

#### How to make it works:

First of all, you need to create a bot in Telegram and get an HTTP API token to connect to it, in order to do so go to BotFather in Telegram (https://t.me/BotFather), create a new bot by following the instructions, give it a name and then you'll get your secret HTTP API token;

Copy and paste the code from "main.py" in this repository in any code editor, the best one is PyCharm Community Edition and thanks to this IDE you can compile the code and check that it doesn't throw any error;

Before to compile you should run 2 simple commands in the console to install the libraries that we need:
* pip install web3
* pip install pyTelegramBotAPI

Note that you have to make 3 small changes to the code before to compile it and before to go ahead with the next and last step:
* line 7: insert your secret HTTP API token generated by BotFather
* line 10, 11, 12: insert the private key compromised and its relative public key, insert also the safe receiver address where you want the bot to send your tokens from the compromised wallet
* line 15: insert your blockchain API KEY to be able to connect to the desired chain, by default in this code is Sepolia testnet
* line 18: insert the actual address of the token smart contract that you want to transfer out from the compromised wallet
* line 144: make sure to change the chainId paramenter accordingly to the network where you want to run this bot, by default in this code is Sepolia testnet

Now it's time to bring the code on a server in order to make the bot actually running, to do so I've created an account on "https://www.pythonanywhere.com/", once you have your account ready to go just simply create a new Python file in "Files" and copy and paste the code. PythonAnywhere is a cool solution to test bots because it's free and it doesn't stop running, in the worst case scenario it simply slows your server, so this solution is perfect for what we need to do;

Once you have copied the code in the file in PythonAnywhere you have to repeat the two "pip install" commands, PythonAnywhere provides you a bash console that let you run your pip commands;

The bot is READY! Go back to BotFather, click on the link to your telegram bot and enjoy it 🤖

* #### How the bot works:

The main functionality of this bot is the /rescue command, when you launch this command, if every parameters/variables have been setted properly, it will make the bot to check evert 5 seconds if the specific token that you want to rescue from the compromised wallet have been actually deposited into the compromised wallet, if no it will run the check again, if yes it will immediately trigger a raw transaction using the private key of the compromised wallet to sign a transfer toward the safe receiver address of all the tokens that have been just deposited into the compromised wallet. All in a matter of 20 seconds at maximum;

The /test command serves only to check directly in the telegram bot chat if all the variables have been setted properly;

#### Note: This code is for educational purposes and intended to demonstrate the basic functionality of a cryptocurrency wallet bot. It should not be used in production without considering additional security measures and proper error handling.
