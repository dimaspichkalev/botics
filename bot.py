# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


updater = Updater(token='875476550:AAHMX4LaLDpsh8oWcQNw7yieufZEA_7T8p4') # Токен API к Telegram
dispatcher = updater.dispatcher


# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, пообщайся со мной)')
def textMessage(bot, update):
    response = 'Ты мне написал: ' + update.message.text + ', ты что офигел????????'
    bot.send_message(chat_id=update.message.chat_id, text=response)

def main():
	# Хендлеры
	start_command_handler = CommandHandler('start', startCommand)
	text_message_handler = MessageHandler(Filters.text, textMessage)
	# Добавляем хендлеры в диспетчер
	dispatcher.add_handler(start_command_handler)
	dispatcher.add_handler(text_message_handler)
	# Начинаем поиск обновлений
	updater.start_polling(clean=True)
	# Останавливаем бота, если были нажаты Ctrl + C
	updater.idle()


if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()