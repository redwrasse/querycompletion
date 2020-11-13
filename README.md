query completion
---

Query completion from a collection of next-character LSTM models.

### Background
Ref www.redwrasse.io/supplementals/querycompletion

Query completion can be factored into a product of next-character models

`P(x_c|x_q) = \prod_i=m-1 to n P(x_i|x_1:i-1)` 

given a query `x_q = x_1...x_m := x_1:m` and a completion `x_c = x_m+1:n`

### Run

start command line prompt
``` 
python3 lstm_query_completion.py
```

![query completion](./resources/querycompl.png)
