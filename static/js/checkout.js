paypal.Buttons({
    createOrder: function (data, actions) {
        return actions.order.create({purchase_units: [{amount: {value: '284.41',},}]});
    }, onApprove: function (data, actions) {
        return actions.order.capture().then(function (details) {
            alert('Transaction completed by ' + details.payer.name.given_name);
            send_success("prime", 6, 284.41);
            return 200;
        });
    }
}).render('#checkout_div_6_prime');
paypal.Buttons({
    createOrder: function (data, actions) {
        return actions.order.create({purchase_units: [{amount: {value: '474.81'}}]});
    }, onApprove: function (data, actions) {
        return actions.order.capture().then(function (details) {
            alert('Transaction completed by ' + details.payer.name.given_name);
            send_success("prime", 12, 474.81);
            return 200;
        });
    }
}).render('#checkout_div_12_prime');
paypal.Buttons({
    createOrder: function (data, actions) {
        return actions.order.create({purchase_units: [{amount: {value: '141.61'}}]});
    }, onApprove: function (data, actions) {
        return actions.order.capture().then(function (details) {
            alert('Transaction completed by ' + details.payer.name.given_name);
            send_success("pro", 6, 141.61);
            return 200;
        });
    }
}).render('#checkout_div_6_pro');
paypal.Buttons({
    createOrder: function (data, actions) {
        return actions.order.create({purchase_units: [{amount: {value: '236.81'}}]});
    }, onApprove: function (data, actions) {
        return actions.order.capture().then(function (details) {
            alert('Transaction completed by ' + details.payer.name.given_name);
            send_success("pro", 12, 236.81);
            return 200;
        });
    }
}).render('#checkout_div_12_pro');

function send_success(package, months, amount) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (this.responseText === "CORRECT") {
                $(document.getElementById("campaign_listing_" + campaign_id)).addClass("hidden")
            }
        }
    };
    xhttp.open("POST", "/api/booked_package", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    data = {package: package, months: months, amount: amount,};
    console.log(JSON.stringify(data));
    xhttp.send(JSON.stringify(data));
}