from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score
from corus import load_corpora
import pickle
import os


class UnigramMorphAnalyzer:
    def __init__(self):
        self.endings_stat = {}
        self.path = os.path.abspath('annot.opcorpora.xml.byfile.zip')
        self.records = []
        self.possible_grams = []
        self.train_data = {
            'token_text': [],
            'token_grams': [],
        }
        self.test_data = {
            'token_text': [],
            'token_grams': [],
        }

    def train(self):

        self.records = load_corpora(self.path)

        tokens = []
        grams = []
        for rec in self.records:
            for par in rec.pars:
                for sent in par.sents:
                    for token in sent.tokens:
                        tokens.append(str(token.text))
                        grams.append(token.forms[0].grams[0])

                    train_test_split_result = train_test_split(
                        tokens, grams,
                        test_size=0.2,
                        train_size=0.8,
                        shuffle=False,
                    )
                    self.train_data['token_text'] = train_test_split_result[0]
                    self.test_data['token_text'] = train_test_split_result[1]
                    self.train_data['token_grams'] = train_test_split_result[2]
                    self.test_data['token_grams'] = train_test_split_result[3]

                    for token, p_speech in zip(
                            self.train_data['token_text'],
                            self.train_data['token_grams']
                    ):
                        for i in range(1, 5):
                            ending = token[-i:]
                            if ending in self.endings_stat:
                                if p_speech in self.endings_stat[ending]:
                                    self.endings_stat[ending][p_speech] += 1
                                else:
                                    self.endings_stat[ending][p_speech] = 1
                            else:
                                self.endings_stat[ending] = {
                                    p_speech: 1
                                }
        self.possible_grams = set(self.train_data['token_grams'])
        return self.endings_stat

    def predict(self, token):
        pos = None
        for i in range(4, 0, -1):
            pos = self.endings_stat.get(token[-i:], None) or None
            if pos is not None:
                break
        if pos is None:
            return {
                gram: 100. / len(self.possible_grams) for gram in self.possible_grams
            }

        max_res = sum(pos.values())
        prediction = {}

        for name, amount in pos.items():
            prediction[name] = amount * 100 / max_res

        return prediction

    def save(self):
        with open('endings.pickle', 'wb') as f:
            pickle.dump(self.endings_stat, f)

    def load(self):
        with open('endings.pickle', 'rb') as f:
            self.endings_stat = pickle.load(f)

    def __getitem__(self, key):
        return self.endings_stat.get(key, None)

    def eval(self):
        result = []
        for test_token in self.test_data['token_text']:
            prediction = self.predict(test_token)
            result.append(
                max(prediction, key=prediction.get)
            )
        return precision_score(self.test_data['token_grams'], result, average='macro', zero_division=1)


reader = UnigramMorphAnalyzer()
print(reader.train())
reader.save()
reader.load()
print(reader.eval())
print(reader['ый'])

test = [
    'Привет', ',', 'это', 'тестовые', 'данные',
    'для', 'проверки', ',', 'надеюсь', 'всё', 'хорошо', '.',
    'Ты', 'хороший', 'человек',
]

for token in test:
    print(f'token: {token} -> {reader.predict(token)}')