# main.py
from flask import Flask, render_template
import json

from lstm_query_completion import load_models, \
    query_completions

app = Flask(__name__)
models = load_models()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/query/<prefix>')
def query(prefix):
    query = prefix
    completions, lstm_probs = query_completions(models, query, 3)
    return make_data_obj(completions, lstm_probs)


def make_data_obj(completions, lstm_probs):
    data_obj = []
    for cpl, prob in sorted(completions.items(), key=lambda e: -e[1]):
        d = dict()
        d["total"] = cpl
        d["likelihood"] = float(prob)
        d["terms"] = []
        for c, lstm_cpl, lstm_prob in sorted(lstm_probs[cpl],
                                             key=lambda e: len(e[1])):
            n = len(lstm_cpl)
            prefix = lstm_cpl
            completion = c
            term_likelihood = lstm_prob
            terms_d = {
                "n": n,
                "prefix": prefix,
                "completion": completion,
                "likelihood": float(term_likelihood)
            }
            d["terms"].append(terms_d)
        data_obj.append(d)
    return json.dumps(data_obj)


if __name__ == '__main__':
    app.run()


