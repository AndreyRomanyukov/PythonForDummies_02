var urlServer = "http://localhost:12345/server"
var getUrl = window.location;
var hostUrl = getUrl.protocol + "//" + getUrl.host;

var lblFeedback = $('#divFeedback');

$(window).load(function () {
    init();
});


function init() {

}


$(document).on('click', '#btnDelete', function () {
    deleteArtist();
});


$(document).on('click', '#btnCancel', function () {
    window.location.replace(hostUrl + "/artists/");
});


function deleteArtist() {
    var artistID = getUrl.pathname.substring(getUrl.pathname.lastIndexOf('/') + 1);

    ajaxDataProvider.deleteArtist(artistID, function (result) {
        window.location.replace(hostUrl + "/artists/");
    });
}

