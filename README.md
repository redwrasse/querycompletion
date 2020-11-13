query completion
---

Query completion from a collection of next-character LSTM models. Weights for some pre-trained models for n = ... are included.
You will need a contiguous sequence of n= models trained to perform query completion.

### Background
See www.redwrasse.io/supplementals/querycompletion 
Query completion can be factored into a product of next-character models.


### Run

start command line prompt
``` 
python3 lstm_query_completion.py
```
----
![query completion](./resources/querycompl.png)
