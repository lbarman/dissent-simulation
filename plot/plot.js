_ = require('underscore');
fs = require('fs')

fs.readFile('datapoints.json', 'utf8', function (err,inputData) {
  if (err) {
    return console.log(err);
  }
  data = _.chain(JSON.parse(inputData));
  b = data.groupBy(s => s.experiment)
  c = b.map(obj => [obj[0].experiment, _.map(obj, i => i.mean * 1000)])
  d = c.map(obj => [obj[0], stats(obj[1])])
  e = d.map(obj => _.flatten(obj))
  f = e.map(obj => list2Gnu(obj))
  h = f.value().join("\r\n")
  console.log(h);
});

function stats(arr) {
    var m = Math.round(mean(arr))
    var v = Math.round(variance(arr))
    return [m, v];
}

function sum(x) {
    var value = 0;
    for (var i = 0; i < x.length; i++) {
        value += parseInt("" + x[i]);
    }
    return value;
}

function mean(x) {
    if (x.length === 0) return null;
    return sum(x) / x.length;
}

function min(x) {
    var value;
    for (var i = 0; i < x.length; i++) {
        if (x[i] < value || value === undefined) value = x[i];
    }
    return value;
}

function max(x) {
    var value;
    for (var i = 0; i < x.length; i++) {
        if (x[i] > value || value === undefined) value = x[i];
    }
    return value;
}

function variance(x) {
    if (x.length === 0) return null;
    var mean_value = mean(x),
        deviations = [];
    for (var i = 0; i < x.length; i++) {
        deviations.push(Math.pow(x[i] - mean_value, 2));
    }
    var std = mean(deviations);
    var sterr = Math.sqrt(std)
    var z_value_95 = 1.96
    var margin_error = sterr * z_value_95
    return margin_error;
}


function list2Gnu(arr) {
    return arr.join(",\t")
}