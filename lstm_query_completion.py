import numpy as np
import random
import tensorflow.keras as keras
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import ModelCheckpoint
import logging


WAR_AND_PEACE = './warandpeace.txt'


logger = logging.getLogger("root")


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


class NextCharLSTM:

    def __init__(self, n):
        self.n = n
        self.filepath = f"weights.bestn={self.n}.hdf5"
        logging.info(f"initialized lstm {n}")
        self.model = self.get_model()

    def get_model(self):
        try:
            model = keras.models.load_model(self.filepath)
            print(f'loaded LSTM model for n={self.n} from checkpoint')

        except Exception as e:
            print(e)
            model = self.__build_model()
            print(f'built new model for n={self.n}')
        return model

    def __build_model(self):
        model = keras.Sequential([
            keras.Input(shape=(self.n, 256)),
                    LSTM(128),
                    Dense(256, activation='softmax'),
            ])
        optimizer = keras.optimizers.RMSprop(learning_rate=0.01)
        model.compile(loss='categorical_crossentropy', optimizer=optimizer)
        return model

    def sample_next_char_pred(self, text):
        i = random.randint(0, len(text) - 1)
        sentence = text[i]
        if len(sentence) > self.n:
            j = random.randint(0, len(sentence) - self.n)
            query = sentence[j:j + self.n]
            dist = self.next_char_dist(query)
            nextchar = chr(np.argmax(dist))
            return nextchar

    def next_char_dist(self, query):
        return get_next_char_dist(query, self.model, self.n)

    def train(self, text, nepochs):
        checkpoint = ModelCheckpoint(filepath=self.filepath,
                                     verbose=0, mode='max')
        callbacks_list = [checkpoint]
        batch_size = 128
        max_length = 10**4
        for epoch in range(nepochs):
            x = np.zeros((max_length, self.n, 256), dtype=np.bool)
            y = np.zeros((max_length, 256), dtype=np.bool)
            k = 0
            random.shuffle(text)
            for i, sentence in enumerate(text):
                for j, c in enumerate(sentence[:-self.n]):
                    query = sentence[j:j + self.n]
                    nextchar = sentence[j + self.n]
                    for t, qc in enumerate(query):
                        if ord(qc) < 256:
                            x[k, t, ord(qc)] = 1
                    if ord(nextchar) < 256:
                        y[k, ord(nextchar)] = 1

                    k += 1

            history = self.model.fit(x, y, batch_size=batch_size, epochs=1,
                                validation_split=0.5,
                                callbacks=callbacks_list, verbose=0)
            loss = history.history['loss'][0]
            val_loss = history.history['val_loss'][0]
            print(f'epoch loss: {loss} epoch val loss: {val_loss}')


def get_next_char_dist(query, model, n):
    x_pred = np.zeros((1, n, 256))
    for t, qc in enumerate(query):
        if ord(qc) < 256:
            x_pred[0, t, ord(qc)] = 1
    dist = model.predict(x_pred, verbose=0)[0]
    return dist


def query_completions(models, query, completion_length, prob_cutoff=1e-2):
    # completion_length is total length of added characters to query
    n_values = sorted([m.n for m in models])
    m = len(query)
    # need lstms from n = m to n = completion_length + m
    for i in range(m, completion_length + m):
        if i not in n_values:
            print(f'missing lstm for n = {i} to perform desired completion')
            return

    lstm_probs = {}
    completion_probs = {query: 1.0}
    for k in range(m, completion_length + m):
        model = [mdl for mdl in models if mdl.n == k][0]
        keys = list(completion_probs)
        for cpl in keys:
            dist = model.next_char_dist(cpl)
            for ix in dist.argsort()[::-1]:
                if completion_probs[cpl] * dist[ix] > prob_cutoff:
                    if cpl not in lstm_probs:
                        lstm_probs[cpl] = []
                    c = chr(ix)
                    next_cpl = cpl + c
                    completion_probs[next_cpl] = completion_probs[cpl] * dist[ix]
                    lstm_probs[next_cpl] = lstm_probs[cpl] + [(c, cpl, dist[ix])]
            del completion_probs[cpl]
        #print(completion_probs)
    return completion_probs, lstm_probs


def load_nextcharlstm_objs():
    import os
    print("loading models ...")
    nextcharlstm_objs = []
    fnames = os.listdir('./')
    for fname in fnames:
        if fname.endswith('.hdf5'):
            n = int(fname.split('.hdf5')[0].split("=")[-1])
            nextcharlstm_objs.append(NextCharLSTM(n))
    print("-"*50)
    return nextcharlstm_objs


def train_n(n):
    text = prepare_war_and_peace()
    lstm = NextCharLSTM(n)
    lstm.train(text, nepochs=100)


