query completion
---
Query completion can be factored into a product of next-character models. In this case a collection of next-character LSTM models. 

Mathematically the query completion probability is the product of next-character probabilities. See references.

For example, completing ‘ora’ with ‘nge’ to make ‘orange’

P(nge|ora) = P(e|orang) P(g|oran) P(n|ora)

Weights for some pre-trained models for n = ... are included.
You will need a contiguous sequence of trained n= models trained to perform query completion.


### Run

start command line prompt

``` 
python3 cmd_line.py
```
----

### Screenshot

![query completion](./resources/cmdline.png)


### References
* [Internal Notes](https://www.redwrasse.io/supplementals/querycompletion)
* [Realtime query completion via deep language models](https://sigir-ecom.github.io/ecom18Papers/paper24.pdf)
