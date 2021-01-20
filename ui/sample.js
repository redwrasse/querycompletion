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

function buildTable(labels, objects, container) {
  var table = document.createElement('table');
  var thead = document.createElement('thead');
  var tbody = document.createElement('tbody');

  var theadTr = document.createElement('tr');
  for (var i = 0; i < labels.length; i++) {
    var theadTh = document.createElement('th');
    theadTh.innerHTML = labels[i];
    theadTr.appendChild(theadTh);
  }
  thead.appendChild(theadTr);
  table.appendChild(thead);

  for (j = 0; j < objects.length; j++) {
    var tbodyTr = document.createElement('tr'); // table row
    for (k = 0; k < labels.length; k++) {
      var tbodyTd = document.createElement('td'); // row element data
      tbodyTd.innerHTML = objects[j][labels[k].toLowerCase()];
      tbodyTr.appendChild(tbodyTd); // append row element data to table row
    }
    tbody.appendChild(tbodyTr); // append table row to table body
  }
  table.appendChild(tbody); // append table body to table

  container.appendChild(table);
}

var labels1 = ['ID', 'Name'];
var objects1 = [
  {"id": "1", 'name': "richard"},
  {"id": "2", 'name': "santos"}
];

var labels2 = ['ID', 'NOME'];
var objects2 = [
  {"id": "1", 'nome': "richard"},
  {"id": "2", 'nome': "adriana"}
];

var labels3 = ['Completion', 'Likelihood', 'Terms'];
var objects3 = [
  {"completion": "which", "likelihood": "21.90%"},
 {"completion": "what", "likelihood": "17.29%"},
    {"completion": "who, ", "likelihood": "13.05%"},
    {"completion": "while", "likelihood": "11.12%"}
];


buildTable(labels3, objects3, document.getElementById('results'));
