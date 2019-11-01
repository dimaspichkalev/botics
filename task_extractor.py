import pymorphy2
from nltk import ngrams
from nltk.corpus import stopwords


def init_non_stop_words(data_dict):
    non_stop_words = []
    for key in data_dict.keys():
        for value in data_dict[key]:
            for split_value in value.split():
                if split_value not in non_stop_words:
                    non_stop_words.append(split_value)
    return non_stop_words


class TaskExtractor:

    def __init__(self, data_dict):
        """
        Конструктор класса TaskExtractor
        :param data_dict: выборка задач бота и их синонимов в виде коллекции (dict)
        """
        self.morph = pymorphy2.MorphAnalyzer()
        self.stop_words = stopwords.words('russian')
        self.data_dict = data_dict
        self.non_stop_words = init_non_stop_words(self.data_dict)

    def extract_tasks(self, input_phrase):
        """
        Алгоритм извлечения задач из сообщения пользователя
        :param input_phrase: сообщение пользователя
        :return: выделенные задачи бота
        """
        preprocess_input, res_ngrams, extracted_tasks = '', [], []
        for w in input_phrase.split():
            if w.strip() not in self.stop_words:
                if self.morph.parse(w)[0].normal_form in self.non_stop_words:
                    preprocess_input += self.morph.parse(w)[0].normal_form + " "

        preprocess_input = preprocess_input.strip()

        for i in range(1, preprocess_input.split().__len__() + 1):
            n_grams = ngrams(preprocess_input.split(), i)
            for grams in n_grams:
                temp = ""
                for j in range(grams.__len__()):
                    temp += grams[j] + " "
                res_ngrams.append(temp.strip())

        tmp = False

        for task, synonyms in self.data_dict.items():
            if preprocess_input in self.data_dict[task]:
                extracted_tasks.append(str(task))
                tmp = True

        if not tmp:
            for gram in res_ngrams:
                for task, synonyms in self.data_dict.items():
                    for synonym in self.data_dict[task]:
                        if gram in synonym:
                            if task not in extracted_tasks:
                                extracted_tasks.append(str(task))

        extracted_string = ' '.join(extracted_tasks)
        return extracted_string