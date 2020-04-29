function set_langauge_to(abbr) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "CORRECT") {
                // $("#campaign_"+campaign_identifier).addText('hidden');
                document.location.href = buildNewHREF(abbr.toString());
                console.log("TRUE")
            }
        }
    };
    xhttp.open("POST", "/api/set_language", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    data = {
        abbr: abbr
    };
    console.log(JSON.stringify(data));

    xhttp.send(JSON.stringify(data));
}

function buildNewHREF(targetLang) {
    var elements = document.location.href.split("/");

    console.log(elements);
    console.log(document.location);

    var path = "/" + targetLang;

    for (var index = 4; index < elements.length; index++) {
        console.log(path);
        console.log(elements[index]);
        path += "/" + elements[index]
    }

    return path;
}