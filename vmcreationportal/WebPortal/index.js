var express = require('express');
var bodyParser = require('body-parser');
var path = require('path');
var db = require('./queries');

var router = express.Router();

var app = express();

app.use(bodyParser.json({
    type: 'application/json',
    limit: '5mb'
}));

var options = {
	index: false
}

router.use(express.static(__dirname + '/public',options));

router.get('/', function(req, res) {
    db.checkBusy(function(busy){
    if (busy === 0) {
        res.sendFile(__dirname + '/public/index.html');
    } else {
        res.sendFile(__dirname + '/public/busy.html');
    }
    });  
});

router.post('/api/login', db.login);
router.post('/api/vm', db.createvm);

app.use(router);
app.listen(3000);
