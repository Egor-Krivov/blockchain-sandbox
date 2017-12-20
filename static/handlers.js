
var host = '192.168.1.49:5000';

var publicKey, privateKey, name;
var keys; 

document.addEventListener("DOMContentLoaded", function() {
    "use strict";

    document.getElementById("create-key").addEventListener("click", handleCreateKeyPairClick);
    document.getElementById("create-transaction").addEventListener("click", handleTransactionClick);
    document.getElementById("table-update").addEventListener("click", handleTableClick);

    // Key pair creation section
    function handleCreateKeyPairClick() {

        var nickname = document.getElementById("inputNickname").value;
        if (!nickname) {
            return;
        }
        name = nickname;
        var rsa = forge.pki.rsa;

        keys = rsa.generateKeyPair({bits: 1024, e: 0x10001});
        publicKey = keys.publicKey;
        privateKey = keys.privateKey;

        var xhttp = new XMLHttpRequest();
        var ip = location.host;
        if (ip === 'localhost:5000') {
            host = ip;
        }
        xhttp.open("POST", "http://" + host + "/user/registration", true);
        xhttp.setRequestHeader("Content-type", "application/json");
        var data = JSON.stringify({'name': name, 'publicKey': forge.pki.getPublicKeyFingerprint(publicKey, {encoding: 'hex'})});
        xhttp.send(data);

        xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4 && xhttp.status === 401) {
            var json = JSON.parse(xhttp.responseText);
            if (json.message === 'Such name already exists') {
                var newDiv = document.createElement("div");
                newDiv.className = "alert alert-danger alert-dismissible fade show align-middle";
                newDiv.idName = 'alert';
                newDiv.style.width = '330px';
                newDiv.style.margin = 'auto';
                    // add the newly created element and its content into the DOM 
                var currentDiv = document.getElementById("balance"); 

                newDiv.innerHTML = '<strong>Such name already exists.</strong><button type="button" class="close" data-dismiss="alert" aria-label="Close"> <span aria-hidden="true">&times;</span></button>';
                document.body.insertBefore(newDiv, currentDiv);
            }
        } 

        if  (xhttp.readyState === 4 && xhttp.status !== 401) {

            updateBalance();
            hideField();
        }};

    }

    function handleTransactionClick() {

        var recipient = document.getElementById("inputRecipient").value;
        var amount = document.getElementById("inputSum").value;
        if (!recipient || !amount) {
            return;
        }
        document.getElementById("inputRecipient").value = null;
        document.getElementById("inputSum").value = null;

        var plaintext = name + recipient + amount;
        //var sign = keys.signString(plaintext, "sha256");

        var md = forge.md.sha256.create();
        md.update('plaintext', 'utf8');
        var sign = privateKey.sign(md);


        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "http://" + host + "/transactions/new", true);
        xhttp.setRequestHeader("Content-type", "application/json");
        var data = JSON.stringify({'sender': name, 'recipient':recipient, 'amount':amount, 'sign': sign});
        xhttp.send(data);

        xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4 && xhttp.status === 404) {
            var json = JSON.parse(xhttp.responseText);
            if (json.message === 'No such recipient') {
                var newDiv = document.createElement("div");
                newDiv.className = "alert alert-danger alert-dismissible fade show align-middle";
                newDiv.idName = 'alert';
                newDiv.style.width = '330px';
                newDiv.style.margin = 'auto';
                    // add the newly created element and its content into the DOM 
                var currentDiv = document.getElementById("transaction-list"); 

                newDiv.innerHTML = '<strong>No such recipient!</strong><button type="button" class="close" data-dismiss="alert" aria-label="Close"> <span aria-hidden="true">&times;</span></button>';
                document.body.insertBefore(newDiv, currentDiv);
            }
        }};

        updateBalance(); 

    };


    function handleTableClick() {

        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "http://" + host + "/user/transactions", true);
        xhttp.setRequestHeader("Content-type", "application/json");

        var data = JSON.stringify({'name': name});
        xhttp.send(data);

        xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4 && xhttp.status === 200) {
            var json = JSON.parse(xhttp.responseText);
            var text = "";
            for(var key in json) {
                text = text + '<tr>';
                var transaction = json[key];
                
                text = text + '<td>';
                text = text + transaction['sender'];
                text = text + '</td>';

                text = text + '<td>';
                text = text + transaction['recipient'];
                text = text + '</td>';

                text = text + '<td>';
                text = text + transaction['amount'];
                text = text + '</td>';

                text = text + '<td>';
                text = text + transaction['n_blocks'];
                text = text + '</td>';
                
                text = text + '</tr>';
            }

            var place = document.getElementById("transactions");
            place.innerHTML = text;
        }};

        updateBalance(); 
        
    };
});

function updateBalance() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "http://" + host + "/user/balance", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    var data = JSON.stringify({'name': name});
    xhttp.send(data);

    xhttp.onreadystatechange = function () {
    if (xhttp.readyState === 4 && xhttp.status === 200) {
        var json = JSON.parse(xhttp.responseText);
        var sum = json.balance;
        document.getElementById("showBalance").innerHTML = '<p>Name: ' + name + '</p>' + '<p>Balance: ' + sum + '</p>';
    }};

};

function sendKey() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "http://localhost:5000/user/registration_key", true);
    xhttp.setRequestHeader("Content-type", "multipart.form-data");

    var formdata = new FormData();
    formdata.append('key', forge.pki.publicKeyToPem(publicKey));
    xhttp.send(formdata);   
}