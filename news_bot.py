import websocket
import json
from websocket_server import WebsocketServer as ws
from threading import Thread
import telebot


url = 'wss://stream.data.alpaca.markets/v1beta1/news'
apiKey = "AKB8JZQ7OQ4WNSM7G78A"
apiSecret = "Yjk3K6rMDBcsbiwBArh90n6XqQmpKAH4f2YdIt1H"
symbols = ['TSLA']
top30_tech = ['TSLA', 'AAPL', 'MSFT', 'GOOG', 'AMZN','TSLA', 'FB', 'NVDA', 'TSM', 'TCEHY', 'BABA', 'ASML', 'AVGO', 'CSCO', 'ORCL', 'ADBE', 'CRM', 'INTC', 'AMD', 'TXN', 'QCOM', 'NFLX', 'QCOM', 'INTU', 'PYPL', 'SAP', 'MPNGF', 'SONY', 'IBM', 'KYCCF', 'NOW']
chat_id = 5144939393
bot = telebot.TeleBot("5277483668:AAEbXVk3fwqfFw10yg-DT47ClTQ6GtXkLRg", parse_mode=None)



@bot.message_handler(commands=['add'])
def send_welcome(message):
    global symbols, chat_id
    chat_id = message.chat.id
    if message.text[5:] in symbols :
        bot.send_message(message.chat.id, f"{message.text[5:]} already exists")
    else:  
        if symbols == ['*']:
            bot.send_message(message.chat.id, 'you selected all the symbols /clear to remove all the symbols')
        else: 
            symbol = f'{message.text[5:]}'
            symbols.append(symbol)
            print(symbols)
            new_subscription([symbol])
            bot.send_message(message.chat.id, f'Symbol {symbol} added')

@bot.message_handler(commands=['remove'])
def send_welcome(message):
    global symbols, chat_id
    chat_id = message.chat.id
    symbol = f'{message.text[8:]}'
    try:
        symbols.pop(symbols.index(symbol))
        print(symbols)
        new_unsubscription(symbol)
        bot.send_message(message.chat.id, f"Symbol {symbol} removed")
    except:
        bot.send_message(chat_id, 'Symbol not in list')
    
@bot.message_handler(commands=['select_all'])
def send_welcome(message):
    global symbols, chat_id
    chat_id = message.chat.id
    symbols = ['*']
    new_subscription(['*'])
    bot.send_message(message.chat.id, f'All symbols selected')

@bot.message_handler(commands=['clear'])
def send_welcome(message):
    global symbols, chat_id
    chat_id = message.chat.id
    symbols = ['TSLA']
    new_unsubscription('*')
    bot.send_message(message.chat.id, f'All symbols cleared')

@bot.message_handler(commands=['info'])
def send_welcome(message):
	bot.send_message(message.chat.id, "This is Basso's News Bot:                                                             /add (Symbol) to add a new specific stock or crypto symbols             /select_all to select all the stock and crypto symbols          /clear to remove all selected stock and crypto symbols           /remove (Symbol) to remove a specific stock or crypto symbols                   /my_symbols yo see your selected symbols                       /info to get info about the bot")


@bot.message_handler(commands=['top_tech'])
def send_welcome(message):
    global symbols, chat_id
    chat_id = message.chat.id
    symbols += top30_tech
    symbols = list(dict.fromkeys(symbols))
    new_subscription(top30_tech)
    bot.send_message(message.chat.id, f'Top 30 Tech symbols added')

@bot.message_handler(commands=['top_tech_info'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Top 30 Tech symbols are: " + str(top30_tech))

@bot.message_handler(commands=['my_symbols'])
def send_welcome(message):
    global symbols, chat_id
    chat_id = message.chat.id
    bot.send_message(chat_id, f'Your crypto and stock symbols are: ' + str(symbols))

def on_message(socket, message):
    global apiKey, apiSecret, symbols, chat_id
    message = json.loads(message)
    try:
        if message[0]['msg'] == "connected":
            print("Authenticatin...")
            auth_data = {
                "action": "auth",
                "key": apiKey,
                "secret": apiSecret
            }
            socket.send(json.dumps(auth_data))

        elif message[0]['msg'] == "authenticated":
            try:
                print('Subscribing...')
                subscribe = {
                    "action": "subscribe",
                    "news": ['TSLA']
                }
                socket.send(json.dumps(subscribe))
                print('Subscribed')
            except:
                print('Subscription failed')

    except:
        try:
            print('Sending message...')
            bot.send_message(chat_id=chat_id, text=f'{message[0]["symbols"]} {message[0]["summary"]}') 
            bot.send_message(chat_id=chat_id, text=message[0]['url'])
            print('Message sent')
        except:
            print(message, symbols)


    
def on_open(socket):
    print('Connected')

def on_error(socket, error):
    print(error)

# new subscription--------------------
def new_subscription(symbol):
    try:
        print(f'Subscribing...{symbol}')
        subscribe = {
            "action": "subscribe",
            "news": symbol
        }
        thread.socket.send(json.dumps(subscribe))
        print('Subscribed')
    except:
        print('Subscription failed')
        bot.send_message(chat_id, 'One or more symbols are invalid, try again')
        symbols.pop()

# new unsubscription------------------
def new_unsubscription(symbol):
    try:
        print(f'Unsubscribing...{symbol}')
        unsubscribe = {
            "action": "unsubscribe",
            "news": [symbol]
        }
        thread.socket.send(json.dumps(unsubscribe))
        print('Unsubscribed')
    except:
        print('Unsubscription failed')
        bot.send_message(chat_id, 'One or more symbols are invalid, try again')

class myClass(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        while True:
            try:
                self.socket.run_forever()
            except:
                self.socket = websocket.WebSocketApp( url, on_message=on_message, on_error=on_error, on_open=on_open)
                self.socket.run_forever()


thread = myClass()

bot.polling()
