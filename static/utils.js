function hideField() {

	name = document.getElementById("inputNickname").value;
    if (!name) {
        return;
    }

    var x = document.getElementById("registration");
    x.style.display = "none";

    var x = document.getElementById("balance");
    x.style.display = "block";

    var x = document.getElementById("transaction");
    x.style.display = "block";

    var x = document.getElementById("transaction-list");
    x.style.display = "block";

    var x = document.getElementById("table-transaction");
    x.style.display = "block";
}