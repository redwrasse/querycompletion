import numpy as np
import random
import tensorflow.keras as keras

from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import ModelCheckpoint


WAR_AND_PEACE = './warandpeace.txt'


def prepare_war_and_peace():
    text = []
    with open(WAR_AND_PEACE, 'r') as fl:
        for ln in fl:
            ln_s = ln.lower().strip().replace("\n", " ")
            if len(ln_s) > 0:
                text.append(ln_s)
        # x data: for each sentence, take all
        # partial sequences of all lengths as queries, fill
        # remaining characters up to maxlen with null char
    return text


class LSTMAutocomplete:

    def __init__(self, lstm_dim=10):
        self.null_char = '0'
        self.lstm_dim = lstm_dim
        self.text = self.prepare_data()
        self.maxlen = max(len(s) for s in self.text)
        print(f'maxlen: {self.maxlen}')
        self.model = self.get_model()

    def build_model(self):
        maxlen = max(len(s) for s in self.text)
        model = keras.Sequential([
            keras.Input(shape=(maxlen - 1, 256)),
            LSTM(self.lstm_dim),
            Dense(256, activation='softmax'),
        ])
        optimizer = keras.optimizers.RMSprop(learning_rate=0.01)
        model.compile(loss='categorical_crossentropy', optimizer=optimizer)

        return model

    def get_model(self):
        filepath = "weights.best.hdf5"
        try:
            model = keras.models.load_model(filepath)
            print('loaded model from checkpoint')

        except:
            model = self.build_model()
            print('built new model')
        return model

    def next_char_dist(self, query):
        maxlen = max(len(s) for s in self.text)
        x_pred = np.zeros((1, maxlen - 1, 256))
        k = len(query)
        for t in range(maxlen - 1):
            if t < k:
                char = query[t]
            else:
                char = self.null_char
            o = ord(char)
            if o < 256:
                x_pred[0, t, o] = 1
        model = self.model
        dist = model.predict(x_pred, verbose=0)[0]
        return dist

    def predict_next_char(self, query):
        dist = self.next_char_dist(query)
        index = np.argmax(dist)
        nextchar = chr(index)
        print(f'predicted next char: {nextchar}')
        return nextchar

    def completion_next(self, query, prob):
        prob_cutoff = 1e-1

        if query[-1] in ['!', '?', '.']:
            return [(query, prob)]

        next_completions = []
        dist = self.next_char_dist(query)
        top_two = dist.argsort()[-2:][::-1]
        c1, c2 = chr(top_two[0]), chr(top_two[1])
        for i, c in enumerate([c1, c2]):
            if c != self.null_char:
                next_query = query + c
                next_query_prob = prob * dist[top_two[i]]
                if next_query_prob > prob_cutoff:
                    next_completions.append((next_query, next_query_prob))
        return next_completions

    def ranked_query_completion(self, query):
        print(f'query: {query}')
        prob = 1.
        completions = [(query, prob)]
        for i in range(self.maxlen - len(query)):
            next_completions = self.qc(completions)
            if set(completions) == set(next_completions):
                break
            completions = next_completions
        return completions

    def qc(self, completions):
        all_c = []
        for query, prob in completions:
            all_c += self.completion_next(query, prob)
        return all_c

    def train(self):

        model = self.get_model()
        filepath = "weights.best.hdf5"
        checkpoint = ModelCheckpoint(filepath=filepath,
                                     verbose=0,  mode='max')
        callbacks_list = [checkpoint]
        maxlen = max(len(s) for s in self.text)
        n_epochs = 50
        batch_size = 1200
        #for epoch in range(n_epochs):

        x = np.zeros((len(self.text), maxlen - 1, 256), dtype=np.bool)
        y = np.zeros((len(self.text), 256), dtype=np.bool)
        for i, sentence in enumerate(self.text):
            # randomly sampled sentence subset as 'query'
            if len(sentence) < 2:
                continue
            min_query_length = min(5, len(sentence)-1)
            k = random.randint(min_query_length, len(sentence) - 1)
            l = random.randint(0, len(sentence) - k - 1)
            query = sentence[l:l+k]
            nextchar = sentence[l+k]
            for t in range(maxlen - 1):
                if t < k:
                    char = query[t]
                else:
                    char = self.null_char
                o = ord(char)
                if o < 256:
                    x[i, t, o] = 1
            if ord(nextchar) < 256:
                y[i, ord(nextchar)] = 1
        history = model.fit(x, y, batch_size=batch_size, epochs=n_epochs,
                  validation_split=0.33,
                  callbacks=callbacks_list, verbose=1)
        loss = history.history['loss'][0]
        val_loss = history.history['val_loss'][0]

        print(f'epoch loss: {loss} epoch val loss: {val_loss}')


    @staticmethod
    def prepare_data():
        return prepare_war_and_peace()


def main():
    lstm_ac = LSTMAutocomplete(lstm_dim=128)
    lstm_ac.train()
    query = 'it'
    lstm_ac.predict_next_char(query)
    completions = lstm_ac.ranked_query_completion(query)
    print(completions)


if __name__ == '__main__':
    main()
