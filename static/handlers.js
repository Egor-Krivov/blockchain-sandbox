var publicKey, privateKey, name;
var keys; 

document.addEventListener("DOMContentLoaded", function() {
    "use strict";

    if (!window.crypto || !window.crypto.subtle) {
        alert("Your current browser does not support the Web Cryptography API! This page will not work.");
        return;
    }
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
        var Bits = 1024; 
        keys = cryptico.generateRSAKey(name, Bits);
        publicKey = cryptico.publicKeyString(keys);
        //privateKey = cryptico.privateKeyString(keys);

        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "http://localhost:5000/wallet_register", true);
        xhttp.setRequestHeader("Content-type", "application/json");
        var data = JSON.stringify({'name': name, 'publicKey':publicKey});
        xhttp.send(data);

        updateBalance(); 

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
        var sign = keys.signString(plaintext, "sha256");


        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "http://localhost:5000/transaction", true);
        xhttp.setRequestHeader("Content-type", "application/json");
        var data = JSON.stringify({'name': name, 'recipient':recipient, 'amount':amount, 'sign': sign});
        xhttp.send(data);

        xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4 && xhttp.status === 200) {
            var json = JSON.parse(xhttp.responseText);
            if (json.message === 'fail') {
                var newDiv = document.createElement("div");
                newDiv.className = "alert alert-danger alert-dismissible fade show align-middle";
                newDiv.idName = 'alert';
                newDiv.style.width = '330px';
                newDiv.style.margin = 'auto';
                    // add the newly created element and its content into the DOM 
                var currentDiv = document.getElementById("transaction-list"); 

                newDiv.innerHTML = '<strong>Error!</strong><button type="button" class="close" data-dismiss="alert" aria-label="Close"> <span aria-hidden="true">&times;</span></button>';
                document.body.insertBefore(newDiv, currentDiv);
            }
        }};

        updateBalance(); 

    };


    function handleTableClick() {

        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "http://localhost:5000/transaction_list", true);
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
    xhttp.open("POST", "http://localhost:5000/balance", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    var data = JSON.stringify({'name': name});
    xhttp.send(data);

    xhttp.onreadystatechange = function () {
    if (xhttp.readyState === 4 && xhttp.status === 200) {
        var json = JSON.parse(xhttp.responseText);
        var sum = json.balance;
        document.getElementById("showBalance").innerHTML = 'Balance: ' + sum;
    }};

};

// function updateBalance() {
//     fetch("http://localhost:5000/balance", {
//         method: 'POST',
//         body: JSON.stringify({'name': name})
//     })
//         .then(function (response) {
//             return response.json();
//         })
//         .then(function (json) {
//             var sum = json.balance;
//             document.getElementById("showBalance").innerHTML = 'Balance: ' + sum;
//             console.log(sum);
//         });
// };