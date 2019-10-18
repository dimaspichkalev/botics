# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pandas as pd
from data_work import preprocess_tasks_set
from task_extractor import TaskExtractor


updater = Updater(token='875476550:AAHMX4LaLDpsh8oWcQNw7yieufZEA_7T8p4') # Токен API к Telegram
dispatcher = updater.dispatcher


# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, пообщайся со мной)')

def textMessage(bot, update):
	code_response = extractor.extract_symptoms(update.message.text)
	response = 'Ты мне написал: {0}, из этого я выделил следущее: {1}'.format(update.message.text, code_response)
	bot.send_message(chat_id=update.message.chat_id, text=response)

def main():
	data = pd.read_csv('tasks.csv', sep=';')
	normalized_tasks_set = preprocess_tasks_set(data)
	extractor = TaskExtractor(normalized_tasks_set)
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