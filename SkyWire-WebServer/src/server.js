var express = require("express");
var stylus = require("stylus");
var nib = require("nib");
var request = require("request");

var app = express();
var summerizeUrl = "http://ec2-54-86-17-214.compute-1.amazonaws.com:8081/summerize?url=";

function compile(str, path) {
  return stylus(str)
    .set('filename', path)
    .use(nib())
}
app.set('views', __dirname + '/views')
app.set('view engine', 'jade')
app.use(express.logger('dev'))
app.use(stylus.middleware(
  { src: __dirname + '/public'
  , compile: compile
  }
))
app.use(express.static(__dirname + '/public'))

app.get('/', function (req, res) {
  res.render('index',{ title : 'SkyWire' });
});

app.get('/summary', function (req, res) {
	request(summerizeUrl + req.query.url, function(err, response, body) {
		responseJSON = JSON.parse(body);
		summaryElems = responseJSON.data;
		console.log(summaryElems);
		res.render('index',{ title : 'SkyWire', "summaryElems" : summaryElems});
	});
});

app.listen(8080);