import pandas as pd
from pathlib import Path
from utils.data_work import preprocess_tasks_set, get_all_bot_commands, get_url_by_command_object
from tasks.open_card import get_open_card_task_response

url_get_tasks = 'https://dev.greendatasoft.ru/#/registry/Task/881611'
main_extractor, commands_list = get_all_bot_commands()


def analyze_message(message_text):
	code_response = main_extractor.extract_tasks(message_text)
	response = 'Выполняю команду {0}...\n\n'
	if code_response != '' and code_response in commands_list:
		if code_response == 'open_card':
			task_response = response.format('поиска юр. лиц') + get_open_card_task_response(message_text)
			return task_response
		elif code_response == 'get_tasks':
			response += 'Открыть задачи \n'
			inside_response = url_get_tasks
			task_response = response.format('открытия текущих задач') + inside_response
			return task_response
		elif code_response == 'say_hello':
			task_response = 'Здравствуйте! Чем я могу вам помочь?'
			return task_response
		else:
			response = 'Я увидел команду {0}, применяю универсальный алгоритм, возвращаю ссылку на объект в базе!\n\n'.format(code_response)
			response += get_url_by_command_object(code_response)
			return response
	else:
		return 'Я не знаю такой команды'




