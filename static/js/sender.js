function delete_from_campaign(user_id, campaign_id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "CORRECT") {
                $(document.getElementById("infl_listing_" + user_id)).addClass("hidden")
            }
        }
    };
    xhttp.open("POST", "/api/unpin_user_from_campaign", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    data = {
        user_id: user_id,
        campaign_id: campaign_id
    }
    xhttp.send(JSON.stringify(data));
}

function delete_campaign(campaign_id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "CORRECT") {
                $(document.getElementById("campaign_listing_" + campaign_id)).addClass("hidden")
            }
        }
    };
    xhttp.open("POST", "/api/delete_campaign", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    data = {
        campaign_id: campaign_id
    }

    xhttp.send(JSON.stringify(data));
}

var currentIdentifier;

function pin_influencer_at_campaign(campaign_identifier, remark) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "CORRECT") {
                console.log("added")
            }
        }
    };
    xhttp.open("POST", "/api/pin_influencer", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    data = {
        campaign_id: campaign_identifier,
        influencer_identifier: currentIdentifier,
        remark: document.getElementById("remark").value
    }
    console.log(JSON.stringify(data))

    xhttp.send(JSON.stringify(data));

    $('#pinInfluencer').modal('hide')
}

function delete_cooperation(cooperationIdentifier) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "CORRECT") {
                $("#COOPERATION_" + cooperationIdentifier.toString()).addClass("hidden")
            }
        }
    };
    xhttp.open("POST", "/api/remove_cooperation", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    data = {
        ID: cooperationIdentifier
    }
    console.log(JSON.stringify(data))

    xhttp.send(JSON.stringify(data));
}

function delete_stored_query(identifier) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "CORRECT") {
                $("#stored_query_" + identifier).addClass("hidden")
                console.log("TRUE")
            }
        }
    };
    xhttp.open("POST", "/api/delete_query", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    data = {
        timestamp: identifier
    }
    console.log(JSON.stringify(data))

    xhttp.send(JSON.stringify(data));
}

function send_pwd_reset_request(mail) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "CORRECT") {
                $("#stored_query_" + identifier).addClass("hidden")
                console.log("TRUE")
            }
        }
    };
    xhttp.open("POST", "/api/request_pwd_reset_token", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    data = {
        mail: mail
    }
    console.log(JSON.stringify(data))

    xhttp.send(JSON.stringify(data));

    $("#pwd_reset").modal('hide')
}

function delete_public_camapign(campaign_identifier) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "CORRECT") {
                $("#campaign_" + campaign_identifier).addClass('hidden')
                console.log("TRUE")
            }
        }
    };
    xhttp.open("POST", "/api/delete_public_campaign", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    data = {
        campaign_identifier: campaign_identifier
    }
    console.log(JSON.stringify(data))

    xhttp.send(JSON.stringify(data));
}

function delete_profile_image(img_identifier) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/api/delete_profile_image", true);
    data = {
        img_identifier: img_identifier.toString().split("/")[4]
    }
    console.log(JSON.stringify(data))

    xhttp.send(JSON.stringify(data));
}