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


class SimpleLSTMQueryCompletion:

    def __init__(self, n):
        self.text = prepare_war_and_peace()
        self.n = n
        self.model = self.get_model()

    def get_model(self):
        filepath = f"weights.bestn={self.n}.hdf5"
        try:
            model = keras.models.load_model(filepath)
            print('loaded model from checkpoint')

        except:
            model = self.__build_model()
            print('built new model')
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

    def sample_next_char_pred(self):
        i = random.randint(0, len(self.text) - 1)
        sentence = self.text[i]
        if len(sentence) > self.n:
            j = random.randint(0, len(sentence) - self.n)
            query = sentence[j:j + self.n]
            print(f'sample query: {query}')
            x_pred = np.zeros((1, self.n, 256))
            for t, qc in enumerate(query):
                if ord(qc) < 256:
                    x_pred[0, t, ord(qc)] = 1
            model = self.model
            dist = model.predict(x_pred, verbose=0)[0]
            nextchar = chr(np.argmax(dist))
            print(f'predicted nextchar: {nextchar}')

    def train(self, nepochs):
        filepath = f"weights.bestn={self.n}.hdf5"
        checkpoint = ModelCheckpoint(filepath=filepath,
                                     verbose=0, mode='max')
        callbacks_list = [checkpoint]
        batch_size = 128
        max_length = 10**4
        for epoch in range(nepochs):
            x = np.zeros((max_length, self.n, 256), dtype=np.bool)
            y = np.zeros((max_length, 256), dtype=np.bool)
            k = 0
            random.shuffle(self.text)
            for i, sentence in enumerate(self.text):
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
            self.sample_next_char_pred()


def main():
    sqc = SimpleLSTMQueryCompletion(n=3)
    sqc.train(nepochs=100)


if __name__ == '__main__':
    main()
