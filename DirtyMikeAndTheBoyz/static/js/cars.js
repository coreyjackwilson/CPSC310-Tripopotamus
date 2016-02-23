function clearTable() {
    var Table = document.getElementById("car-table");
    Table.innerHTML = "";
}

function confirmTrip(uberPrice){
    saved = taxiPrice - uberPrice;

    if (saved > 0) {
        document.getElementById("basic-modal-content5").innerHTML = "You're going to save " + "$" + Math.round(saved * 100) / 100;
    } else if (saved < 0) {
        document.getElementById("basic-modal-content5").innerHTML = "You're going to lose " + "$" + Math.round(saved * -100) / 100;
    } else {
        document.getElementById("basic-modal-content5").innerHTML = "You're just going to break even";
    }

    var buttons = document.createElement('span');
    buttons.innerHTML = '<button onclick="sendConfirmTripBack()">CONFIRM</button>';
    document.getElementById("basic-modal-content5").appendChild(buttons);

}

function sendConfirmTripBack() {
    $.get(/userDataTransfer/,
        obj = {"curr": start, "dest": end, "price": saved, "distance": distance},
        function (status) {
        });
    getAmazonItems(totalUserSavings);
}





