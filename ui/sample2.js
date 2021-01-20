
const completion1 = {
    result: "which",
    likelihood: 0.219,
    terms: [
        {n:2, prefix: "wh", completion: "i", likelihood: 0.3429},
        {n:3, prefix: "whi", completion: "c", likelihood: 0.6454},
        {n:4, prefix: "whic", completion: "h", likelihood: 0.9894}
    ]

};

const completion2 = {
    result: "what",
    likelihood: 0.1729,
    terms: [
        {n:2, prefix: "wh", completion: "at", likelihood: 0.174},
        {n:3, prefix: "wha", completion: "t", likelihood: 0.9934},
        {n:4, prefix: "what", completion: " ", likelihood: 0.9999}
    ]

};

const sample = [{
    query: "wh",
    completions: [completion1, completion2]
}];
jdata = [
    {
        "name":"bob",
        "salary":13000,
        "friends":[
            {
                "name": "sarah",
                "salary":10000
            },
            {
                "name": "bill",
                "salary":5000
            }
        ]
    },
    {
        "name":"marge",
        "salary":10000,
        "friends":[
            {
                "name": "rhonda",
                "salary":10000
            },
            {
                "name": "mike",
                "salary":5000,
                "hobbies":[
                    {
                        "name":"surfing",
                        "frequency":10
                    },
                    {
                        "name":"surfing",
                        "frequency":15
                    }
                ]
            }
        ]
    },
    {
        "name":"joe",
        "salary":10000,
        "friends":[
            {
                "name": "harry",
                "salary":10000
            },
            {
                "name": "sally",
                "salary":5000
            }
        ]
    }
];


d3.select("body").selectAll("table")
    .data([sample[0]["completions"]])
    .enter().append("table")
    .call(recurse);

function recurse(sel) {
    // sel is a d3.selection of one or more empty tables
    sel.each(function(d) {
        // d is an array of objects
        var colnames,
            tds,
            table = d3.select(this);

        // obtain column names by gathering unique key names in all 1st level objects
        // following method emulates a set by using the keys of a d3.map()
        colnames = d                                                          // array of objects
            .reduce(function(p,c) { return p.concat(d3.keys(c)); }, [])       // array with all keynames
            .reduce(function(p,c) { return (p.set(c,0), p); }, d3.map())      // map with unique keynames as keys
            .keys();                                                          // array with unique keynames (arb. order)

        // colnames array is in arbitrary order
        // sort colnames here if required

        // create header row using standard 1D data join and enter()
        table.append("thead").append("tr").selectAll("th")
            .data(colnames)
            .enter().append("th")
            .text(function(d) { return d; });

        // create the table cells by using nested 2D data join and enter()
        // see also http://bost.ocks.org/mike/nest/
        tds = table.append("tbody").selectAll("tr")
            .data(d)                            // each row gets one object
            .enter().append("tr").selectAll("td")
            .data(function(d) {                 // each cell gets one value
                return colnames.map(function(k) { // for each colname (i.e. key) find the corresponding value
                    return d[k] || "";              // use empty string if key doesn't exist for that object
                });
            })
            .enter().append("td");

        // cell contents depends on the data bound to the cell
        // fill with text if data is not an Array
        tds.filter(function(d) { return !(d instanceof Array); })
            .text(function(d) { return d; });
        // fill with a new table if data is an Array
        tds.filter(function(d) { return (d instanceof Array); })
            .append("table")
            .call(recurse);
    });
}

