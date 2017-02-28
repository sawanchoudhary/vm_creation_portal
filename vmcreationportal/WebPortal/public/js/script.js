var username; // Username
var password; // Password
var emp_id; // Employee ID
var serverIP = "172.17.200.211"; //IP of server. Used in API calls
var sessionToken;
var displayName;
var mail;


$("#loginForm").submit(function() {
    username = $("#username").val(); //get Username
    username = username.toLowerCase();
    password = $("#password").val(); //get Password
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "http://" + serverIP + ":3000/api/login",
        "method": "POST",
        "headers": {
            "content-type": "application/json",
            "cache-control": "no-cache"
        },
        "processData": false,
        "data": "{\"username\":\"" + username + "\",\"password\":\"" + password + "\"}"
    };

    $.ajax(settings).done(function(response) {
        emp_id = response["Employee ID"];
        sessionToken = response["Session Token"];
        displayName = response["Display Name"];
        mail = response["Email"];
        $("#content").load("form.html", readyForm);
    }).fail(function() {
        toastr.error("Username or Password Incorrect");
    });
    return false;
});

function readyForm() {
    $('#owner').val(displayName);
    $('#email').val(mail);

    $('#logout').on('click', function() {
        window.location.replace("http://" + serverIP + ":3000");
    });

    $('#detailform').submit(function() {
        var packages = [];
        $('input:checked').each(function() {
            packages.push($(this).attr('value'));
        }).promise().done(function() {
            var package_data = '';
            for (i = 0; i < packages.length; i++) {
                package_data = package_data + '"' + packages[i] + '",';
                if (i == packages.length - 1) {
                    package_data = package_data.slice(0, -1);
                }
            }

            var owner = $('#owner').val();
            var email = $('#email').val();
            var pname = $('#pname').val();
            var os = $('#os').val();
            var osversion = $('#osversion').val();
            var vcpu = $('#vcpu').val();
            var ram = parseInt($('#ram').val()) * 1024;
            var storage = parseInt($('#storage').val());

            var vmname = pname + '_' + makeid();

            var owner_data = '"Owner":"' + owner + '","Email":"' + email + '","Project Name":"' + pname + '","Project Start":"01/01/2016","Project End":"31/12/2018"'
            var vm_data = '"VM Name":"' + vmname + '","OS":"' + os + '","OS Version":"' + osversion + '","VCPU":' + vcpu + ',"RAM":' + ram + ',"Storage":' + storage;
            var package_data = '"Packages":[' + package_data + ']';

            var post_data = '{' + owner_data + ',' + vm_data + ',' + package_data + '}';

            var settings = {
                "async": true,
                "crossDomain": true,
                "url": "http://" + serverIP + ":3000/api/vm",
                "method": "POST",
                "headers": {
                    "content-type": "application/json",
                    "cache-control": "no-cache",
                    "x-session-token": sessionToken
                },
                "processData": false,
                "data": post_data
            };

            $.ajax(settings).done(function() {
                $("#content").load("thankyou.html");
            }).fail(function() {
                toastr.error("Some Internal Error Occurred. Our team will be right on it.");
            });
        });
        return false;
    });
}

function makeid() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 5; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}
