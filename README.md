query completion
---

Query completion from a collection of next-character LSTM models. Weights for some pre-trained models for n = ... are included.
You will need a contiguous sequence of n= models trained to perform query completion.

### Background
Query completion can be factored into a product of next-character models.

See www.redwrasse.io/supplementals/querycompletion for details.

Additionally, query completion is a larger topic, 
see for example https://sigir-ecom.github.io/ecom18Papers/paper24.pdf



### Run

start command line prompt
``` 
python3 lstm_query_completion.py
```
----

### Screenshot

![query completion](./resources/querycompl.png)
