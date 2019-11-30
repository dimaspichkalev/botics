import os
from utils.data_work import preprocess_tasks_set
from utils.task_extractor import TaskExtractor
import requests


def prepare_dataset():
	auth_url = os.environ['AUTH_URL']
	auth_data = {
		'j_username': os.environ['GREENDATA_USER'],
		'j_password': os.environ['GREENDATA_PWD']
	}
	get_uriki_url = os.environ['GET_URIKI_URL']
	with requests.Session() as session:
		session.post(auth_url, auth_data)
		response = session.get(get_uriki_url)
	ur_clients = response.json()
	clients_dic = {}
	for client in ur_clients['content']:
		clients_dic[client['values']['ID']['value']] = [client['values']['NAME']['value'].replace('"', '')]
	# data = pd.read_csv('urici.csv', sep=';')
	# data = data.set_index('task').T.to_dict('list')
	normalized_clients_set = preprocess_tasks_set(clients_dic)
	return normalized_clients_set


def get_open_card_task_response(message_text):
	ur_dataset = prepare_dataset()
	inside_extractor = TaskExtractor(ur_dataset)
	client_id = inside_extractor.extract_tasks(message_text)
	client_list = client_id.split(' ')
	response = ""
	if len(client_id) > 0:
		response = "По данному запросу найдены следующие организации: \n\n"
		url_card = "https://dev.greendatasoft.ru/#/card"
		for cid in client_list:
			client_name = ur_dataset[int(cid)]
			response = response + "<button><a href='{0}/{1}' target='_blank'>{2}</a></button>\n\n".format(url_card, cid, client_name)
	else:
		response = "По данному запросу ничего не найдено"
	return response
