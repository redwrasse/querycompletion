// sample query data

const completion1 = {
    total: "which",
    likelihood: 0.219,
    terms: [
        {n:2, prefix: "wh", completion: "i", likelihood: 0.3429},
        {n:3, prefix: "whi", completion: "c", likelihood: 0.6454},
        {n:4, prefix: "whic", completion: "h", likelihood: 0.9894}
    ]

};

const completion2 = {
    total: "what",
    likelihood: 0.1729,
    terms: [
        {n:2, prefix: "wh", completion: "at", likelihood: 0.174},
        {n:3, prefix: "wha", completion: "t", likelihood: 0.9934},
        {n:4, prefix: "what", completion: " ", likelihood: 0.9999}
    ]

};

const sample = {
    query: "wh",
    completions: [completion1, completion2]
};
