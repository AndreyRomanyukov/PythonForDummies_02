var urlServer = "http://localhost:12345/server"
var getUrl = window.location;
var hostUrl = getUrl.protocol + "//" + getUrl.host;

$(window).load(function () {
    init();
});


function init() {

}


$(document).on('click', '.clsBtnAddNewArtist', function () {
    window.location.replace(hostUrl + "/AddArtist/");
});


$(document).on('click', '.clsBtnDeleteArtist', function () {
    artistID = $(this).attr('id');
    window.location.replace(hostUrl + "/DeleteArtist/" + artistID);
});

$(document).on('click', '.clsBtnUpdateArtist', function () {
    artistID = $(this).attr('id');
    window.location.replace(hostUrl + "/UpdateArtist/" + artistID);
});