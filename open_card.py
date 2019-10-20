from task_extractor import TaskExtractor
import pandas as pd
from data_work import preprocess_tasks_set


def prepare_dataset():
	data = pd.read_csv('urici.csv', sep=';')
	data = data.set_index('task').T.to_dict('list')
	normalized_clients_set = preprocess_tasks_set(data)
	return normalized_clients_set

