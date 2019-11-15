import pandas as pd
import os
from data_work import preprocess_tasks_set
from task_extractor import TaskExtractor
from open_card import prepare_dataset

data = pd.read_csv('tasks.csv', sep=';')
data = data.set_index('task').T.to_dict('list')
normalized_tasks_set = preprocess_tasks_set(data)
extractor = TaskExtractor(normalized_tasks_set)
extractors = {'open_card': TaskExtractor(prepare_dataset())}


def analyze_message(message_text):
	code_response = extractor.extract_tasks(message_text)
	response = 'Ты мне написал: {0}, из этого я выделил следущее: {1}\n\n'.format(message_text, code_response)
	return code_response
	if code_response != '':
		if code_response in extractors:
			inside_extractor = extractors[code_response]
			if code_response == 'open_card':
				full_url = get_open_card_user_url(inside_extractor, message_text)
				return response + full_url
			if code_response == 'open_tasks':
				#full_url = get_open_card_user_url(inside_extractor, message_text)
				response = "мне нужно открыть ваши задачи"
				return response
		else:
			return 'Я увидел команду {0}, но не знаю что с ней делать :('.format(code_response)
	else:
		return 'Ничего не понял'
	

def get_open_card_user_url(inside_extractor, message_text):
	client_id = inside_extractor.extract_tasks(message_text)
	url_base = 'https://dev.greendatasoft.ru/#/card/'
	full_url = url_base + str(client_id)
	return full_url

def get_open_user_tasks_url():
	url = 1
