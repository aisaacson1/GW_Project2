npm install git+https://github.com/StratoDem/pandas.js

import { Series, DataFrame } from 'pandas-js';

var Series = require('pandas-js').Series;
var DataFrame = require('pandas-js').DataFrame;

raw_results = d3.json("https://gwprojectflask.herokuapp.com/api/data/raw_results")

const df = new DataFrame(raw_results)

console.log(raw_results)


