from nltk.corpus import stopwords
import pymorphy2

stop_words = stopwords.words('russian')
morph = pymorphy2.MorphAnalyzer()

def preprocess_tasks_set(tasks_set):
    """
    Преобразование выборки задач к колекции (dict) вида {task: [synonyms], task2: [synonyms]}
    :return: коллекция задач и их синонимов
    """
    normalized_dict = {}
    data_dict = tasks_set.set_index('task').T.to_dict('list')
    for task, synonyms in data_dict.items():
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