function getAmazonItems(userTotalSavings) {
    if (userTotalSavings < 0.10 && userTotalSavings > -0.10) {
        notifyNotEnoughSavings();
    }
    else {
        document.getElementById("basic-modal-content5").innerHTML = "";
        $.get(/getAmazonProducts/,
            function (status) {
                var itemArray = JSON.parse(status);
                addSavingsTitleToDiv(userTotalSavings);
                for (var i = 0; i < itemArray.length; i++) {
                    var item = itemArray[i];
                    loadAmazonContent(item, userTotalSavings);
                }
                var amazonDiv = document.getElementById("basic-modal-content5");
                var exitButton = document.createElement('span');
                exitButton.innerHTML = '<button onclick="pageRefresh()">Thanks bra.</button>';
                amazonDiv.appendChild(exitButton);
            });
    }
}

function notifyNotEnoughSavings() {
    document.getElementById("basic-modal-content5").innerHTML = "";
    document.getElementById("basic-modal-content5").innerHTML = "You need to take more trips before you can buy something";
}

function addSavingsTitleToDiv(userTotalSavings) {
    var amazonDiv = document.getElementById("basic-modal-content5");
    if (userTotalSavings < 0) {
        amazonDiv.insertAdjacentHTML('beforeend', "<p>Oh dear, with the amount of money you haven't saved, you could have bought..</p>");
    }
    else {
        amazonDiv.insertAdjacentHTML('beforeend', "<p>Wowzers! with your savings you could buy..</p>");
    }
}

function loadAmazonContent(item, userTotalSavings){
    var amazonDiv = document.getElementById("basic-modal-content5");
    var amount = Math.floor((Math.abs(userTotalSavings) * 100) / item.price );
    var url_content = '<br>' + amount + ' of these '+ '<a href=' + item.amazon_url +'>' + item.title +'</a>';
    var picture_content ='<br>' + '<img src=' + item.picture_url + '>';
    amazonDiv.insertAdjacentHTML('beforeend', picture_content);
    amazonDiv.insertAdjacentHTML('beforeend', url_content);
    amazonDiv.insertAdjacentHTML('beforeend', '\n' + "$" + (item.price/100).toFixed(2));
}

function pageRefresh(){
    location.reload();
}