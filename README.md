query completion
---

Predicting several characters ahead is quite a bit more complicated than predicting one character ahead.
Query completion can be factored into a product of next-character models. In this case a collection of next-character LSTM models. 

Weights for some pre-trained models for n = ... are included.
You will need a contiguous sequence of trained n= models trained to perform query completion.

### Run

start command line prompt
``` 
python3 lstm_query_completion.py
```
----

### Screenshot

![query completion](./resources/querycompl.png)


### References
* www.redwrasse.io/supplementals/querycompletion
* https://sigir-ecom.github.io/ecom18Papers/paper24.pdf
