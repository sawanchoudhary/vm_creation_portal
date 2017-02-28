var ldap = require('ldapjs');
var jwt = require('jsonwebtoken');
var json2csv = require('json2csv');
var fs = require('fs');
var mailer = require('nodemailer');
const exec = require('child_process').exec;

module.exports = {
    login: login,
    createvm: createvm,
    checkBusy: checkBusy
}

var secretKey = 'thisisasupersecretkey';

function checkBusy(callback) {
    fs.readFile(__dirname + '/VM_files/CSV/busy.txt', function(err, data) {
        if (data == '1') {
            callback(1);
	    return;
        } else {
            callback(0);
            return;
        }
    });
}

function verifyToken(req, callback) {
    var token = null;
    token = req.headers['x-session-token'];
    if (token) {
        jwt.verify(token, secretKey, function(err, decoded) {
            if (!err) {
                callback(1);
            } else {
                callback(0);
                return;
            }
        });
    } else {
        callback(0);
        return;
    }
}

function createvm(req, res, next) {
    verifyToken(req, function(appr) {
        if (appr) {
            var result = json2csv({
                data: req.body
            });
            fs.writeFile(__dirname + '/VM_files/CSV/busy.txt', '1', function(err) {
                if (err) {
                    throw err;
                } else {
                    fs.writeFile(__dirname + '/VM_files/CSV/' + req.body["VM Name"] + '.csv', result, function(err) {
                        if (err) {
                            throw err;
                        } else {
                            fs.writeFile(__dirname + '/VM_files/CSV/new_vm_info.txt', req.body["VM Name"] + '.csv', function(err) {
                                if (err) {
                                    throw err;
                                } else {
                                    exec(__dirname + '/VM_files/CSV/./vm_creation_portal_start.sh', function(error, stdout, stderr) {
                                        console.log(stdout);
                                        console.log(stderr);
                                        if (error !== null) {
                                            console.log('exec error: ' + error);
                                        }
                                    });
                                    sendmail(req.body);
                                    return res.sendStatus(201);
                                }
                            });
                        }
                    });
                }
            });
        } else {
            return res.sendStatus(403);
        }
    });
}

function login(req, res, next) {
    var LDAP_IP = '192.168.207.44';
    var LDAP_PORT = '3268';
    var LDAP_BINDDN = 'cn=Ldap Access,ou=it-tech,dc=calsofthq,dc=com';
    var LDAP_PASSWORD = 'Qwerty!23';
    var LDAP_FILTER = 'sAMAccountName';
    var LDAP_BASEDN = 'dc=calsofthq,dc=com';

    if (req.body.username && req.body.password) {
        var client = ldap.createClient({
            url: 'ldap://' + LDAP_IP + ':' + LDAP_PORT
        });

        var opts = {
            filter: '(' + LDAP_FILTER + '=' + req.body.username + ')',
            scope: 'sub'
        };

        client.bind(LDAP_BINDDN, LDAP_PASSWORD, function(err) {
            if (err) {
                console.log(err);
                return res.sendStatus(500);
            } else {
                client.search(LDAP_BASEDN, opts, function(err, resp) {
                    if (err) {
                        console.log(err);
                    } else {
                        var LDAP_USERDN = null;
                        var LDAP_DISPLAYNAME = null;

                        resp.on('searchEntry', function(entry) {
                            LDAP_USERDN = entry.object.dn;
                            LDAP_DISPLAYNAME = entry.object.displayName;
                            LDAP_MAIL = entry.object.mail;
                        });

                        resp.on('end', function(result) {
                            if (!LDAP_USERDN) {
                                return res.sendStatus(401);
                            } else {
                                client.bind(LDAP_USERDN, req.body.password, function(err) {
                                    if (err) {
                                        console.log(err);
                                        return res.sendStatus(401);
                                    } else {
                                        jwt.sign({
                                            username: req.body.username
                                        }, secretKey, {
                                            expiresIn: 86400
                                        }, function(err, token) {
                                            if (!err) {
                                                res.status(200)
                                                    .json({
                                                        'Display Name': LDAP_DISPLAYNAME,
                                                        'Email': LDAP_MAIL,
                                                        'Session Token': token
                                                    });
                                            } else {
                                                console.log("Error gEnRaTiNg token");
                                                return res.sendStatus(500);
                                            }
                                        });
                                    }
                                });
                            }
                        });
                    }
                });
            }
        });
    } else {
        return res.sendStatus(401);
    }
}

function sendmail(options) {
    var config = {
        host: '192.168.206.109',
        port: 587,
        secure: false,
        auth: {
            user: 'monitor',
            pass: 'monitor'
        },
        tls: {
            rejectUnauthorized: false
        }
    };

    var info_table = '<table style="border: 1px solid black;">';
    for (var key in options) {
        if (key != "Project Start" && key != "Project End") {
            info_table = info_table + '<tr><td style="border: 1px solid black;"><b>' + key + '</b></td><td style="border: 1px solid black;">' + options[key] + '</td></tr>';
        }
    }
    info_table = info_table + '</table>';

    var mail_text = 'Hello ' + options["Owner"] + ',<br><br>Your request to create new VM has been successfully registered with the following details.<br><br>' + info_table + '<br>Kindly wait till the VM is up and running.<br>Thank you.';

    var transporter = mailer.createTransport(config);

    var mail_options = {
        from: 'monitor@calsoftinc.com',
        to: options["Email"],
        subject: 'VM Creation Portal',
        html: mail_text
    };

    transporter.sendMail(mail_options, function(error, info) {
        if (error) {
            return console.log(error);
        }
    });
}
