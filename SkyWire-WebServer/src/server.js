var express = require("express");
var stylus = require("stylus");
var nib = require("nib");
var request = require("request");
var async = require("async");
var htmlEntities = require("html-entities").AllHtmlEntities;
var entities = new htmlEntities();

var app = express();
//var summerizeUrl = "http://ec2-54-86-17-214.compute-1.amazonaws.com:8081/summerize?url=";
var summerizeUrl = "http://localhost:8081/summerize";
var googleSearchUrl = "https://www.googleapis.com/customsearch/v1?key=AIzaSyD84EFDTC-UP_0rwon5xCNPXT8ZKhuELOQ&cx=018175008996529345468:pgsdofhw0vs&q=";

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
        var summaryElems = responseJSON.data;
        console.log(summaryElems);
        res.render('index',{ title : 'SkyWire', "summaryElems" : summaryElems});
    });
});

app.get('/search', function (req, res) {
	console.log(req.query.q);
    request(googleSearchUrl + req.query.q, function(err, response, body) {
        responseJSON = JSON.parse(body);
        var summaryItems = [];
        if(responseJSON.items) {
            for(var i = 0; i < responseJSON.items.length; i++) {
                var summaryItem = {};
                summaryItem.title = responseJSON.items[i].htmlTitle;
                summaryItem.link = responseJSON.items[i].link;
                summaryItem.query = req.query.q;
                summaryItems.push(summaryItem);
            }
        }
        console.log(summaryItems);
        async.map(summaryItems, function(summaryItem, cb) {
        	var cSummaryUrl = summerizeUrl + "?url=" + summaryItem.link + "&query=" + summaryItem.query;
        	request(cSummaryUrl, function(error, response, body) {
        		if(!error) {
        			console.log("completed for link : " + summaryItem.link);
        			console.log(response);
        			responseData = JSON.parse(body);
        			summaryItem.data = responseData.data;
        			summaryItem.summary = responseData.summary;
        			cb(null, summaryItem);
        		} else {
        			cb(null, {});
        		}
        	});
        }, function(error, results) {
        	if(!error) {
        		res.render('main-widget',{"summaryItems" : results});
        	} else {
        		res.render('main-widget',{"summaryItems" : []});
        	}
        });
    });
});

app.listen(8080);