var selectPicker = document.getElementById("channelSelect");
var channelSpecificOptions = [
    ["1", document.getElementById("instagramFilters")],
    ["2", document.getElementById("facebookFilters")],
    ["3", document.getElementById("youtubeFilters")],
    ["4", document.getElementById("pinterestFilters")],
    ["5", document.getElementById("blogFilters")]
];

function setChannelSpecificOptions(channelIndex) {
    for (i = 0; i < channelSpecificOptions.length; i++) {
        if (channelSpecificOptions[i][0] !== channelIndex) {
            $(channelSpecificOptions[i][1]).addClass("hidden");
        } else {
            $(channelSpecificOptions[i][1]).removeClass("hidden");
        }
        console.log("SELECTED: " + channelIndex);
    }
}

function save_search() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "CORRECT") {
                $("#save_search_button").addClass("hidden")
                $('#save_query_modal').modal('hide')
            }
        }
    };
    xhttp.open("POST", "/api/save_search", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    data = {
        title: $("#modal_query_title").val(),
        search: document.location.href
    };
    console.log(JSON.stringify(data));

    xhttp.send(JSON.stringify(data));
}

function get_next_20_entries() {
    var url = new URL(document.location.href);

    if (url.searchParams.get("offset") == null) {
        url.searchParams.set('offset', 20);
    } else {
        url.searchParams.set('offset', parseInt(url.searchParams.get("offset")) + 20);
    }
    console.log(url);

    document.location.href = url;
}

function get_previous_20_entries() {
    var url = new URL(document.location.href);

    url.searchParams.set('offset', parseInt(url.searchParams.get("offset")) - 20);

    console.log(url);

    document.location.href = url;
}

function get_entries_of_page(page) {
    var url = new URL(document.location.href);

    url.searchParams.set('offset', parseInt(page) * 20 - 20);
    console.log(url);

    document.location.href = url;
}