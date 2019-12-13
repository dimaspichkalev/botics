from nltk.corpus import stopwords
import pymorphy2
import requests
import os
from utils.task_extractor import TaskExtractor

stop_words = stopwords.words('russian')
morph = pymorphy2.MorphAnalyzer()

auth_url = os.environ['AUTH_URL']
auth_data = {
        'j_username': os.environ['GREENDATA_USER'],
        'j_password': os.environ['GREENDATA_PWD']
        }

def preprocess_tasks_set(tasks_set):
    """
    Преобразование выборки задач к колекции (dict) вида {task: [synonyms], task2: [synonyms]}
    :return: коллекция задач и их синонимов
    """
    normalized_dict = {}
    for task, synonyms in tasks_set.items():
        syn = []
        for s in synonyms:
            synonym = ""
            if isinstance(s, str):
                for token in s.split():
                    if token not in stop_words:
                        synonym += morph.parse(token)[0].normal_form + " "
                syn.append(synonym.strip())
        normalized_dict[task] = list(syn)
    return normalized_dict

def get_all_bot_commands():

    get_command_url = 'https://dev.greendatasoft.ru/api/sys/objTypes/1192802/objects'
    with requests.Session() as session:
        session.post(auth_url, auth_data)
        response = session.get(get_command_url)
    resp = response.json()
    command_dict = {}
    for i in resp['content']:
        element = i['values']['CB_COMMAND_ID']['value'][0]
        if '@id' not in element:
            if element['@ref'] not in command_dict:
                command_dict[element['@ref']] = None
        else:
            command_dict[element['@id']] = element['values']['NAME']['value']
    
    new_dict = {}
    for i in resp['content']:
        element = i['values']['CB_COMMAND_ID']['value'][0]
        task_id = element['@id'] if ('@id' in element) else i['values']['CB_COMMAND_ID']['value'][0]['@ref']
        if command_dict[task_id] not in new_dict:
            new_dict[command_dict[task_id]] = []
        synonim = i['values']['NAME']['value']
        new_dict[command_dict[task_id]].append(synonim)
    normalized_tasks_set = preprocess_tasks_set(new_dict)
    return TaskExtractor(normalized_tasks_set)

def get_commands_url(command_id):

    get_commands_url_link = 'https://dev.greendatasoft.ru/api/sys/objTypes/1210621/objects'

    with requests.Session() as session:
        session.post(auth_url, auth_data)
        response = session.get(get_commands_url_link)

    resp = response.json()
    
    for i in resp['content']:
        element = i['values']['CB_COMMAND_OBJECT_ID']['value'][0]['values']['ID']['value']
        if int(element) == int(command_id):
            return i['values']['NAME']['value']
    return ''
