import telebot
import tweepy

#Токен бота берем из BotFather
token = ""
#бирер твиттера, берем из браузера
bearer = ""

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в бота! Введите /check user чтобы узнать последние подписки пользователя')



@bot.message_handler(commands=["check"])
def handle_text(message):
    try:
        params = message.text.split(" ")
        if len(params) != 2:
            bot.send_message(message.chat.id, 'Команда введена неправильно.')
        else:
            auth = tweepy.OAuth2BearerHandler(bearer)
            api = tweepy.API(auth)
            friends_list= api.get_friends(screen_name =params[1],count=20)
            text = ""
            for friend in friends_list:
                text = text + "\n" + "https://twitter.com/"+ friend.screen_name + "\n"
            bot.send_message(message.chat.id, text)    
    except tweepy.errors.NotFound:
        print(params[0])
        bot.send_message(message.chat.id, 'Такого пользователя не существует.')    
    except tweepy.errors.Unauthorized:
        bot.send_message(message.chat.id, 'Данный пользователь был заблокирован.')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Неизвестная команда.')  

bot.polling(none_stop=True, interval=0)
