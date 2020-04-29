function delete_influencer_profile(influencer_identifier, identifier) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "CORRECT") {
                $("#" + identifier.toString()).addClass("hidden");
            }
        }
    };
    xhttp.open("POST", "/api/adminoptions/delete_influencer_profile", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    data = {
        influencerIdentifier: influencer_identifier
    };
    console.log(JSON.stringify(data));

    xhttp.send(JSON.stringify(data));
}

function ignore_reported_influencer(report_identifier, identifier) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "CORRECT") {
                $("#" + identifier.toString()).addClass("hidden");
            }
        }
    };
    xhttp.open("POST", "/api/admin/ignore_reported_influencer", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    data = {
        report_identifier: report_identifier
    };
    console.log(JSON.stringify(data));

    xhttp.send(JSON.stringify(data));
}