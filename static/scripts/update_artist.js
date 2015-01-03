var getUrl = window.location;
var hostUrl = getUrl.protocol + "//" + getUrl.host;

var lblFeedback = $('#divFeedback');

$(window).load(function () {
    init();
});


function init() {
    lblFeedback = $('#divFeedback');
}


$(document).on('click', '#btnUpdate', function () {
    updateArtist();
});


$(document).on('click', '#btnCancel', function () {
    window.location.replace(hostUrl + "/artists/");
});


function updateArtist() {
    lblFeedback.html("");

    var newName = $('#txtName').val();
    var artistID = getUrl.pathname.substring(getUrl.pathname.lastIndexOf('/') + 1);

    if (newName.length == 0){
        lblFeedback.html("Name must be entered")
    }
    else {
        ifArtistExist(artistID, newName);
    }
}


function ifArtistExist(id, name){
    ajaxDataProvider.ifArtistExist(name, function (result) {
        if (result.result.toLowerCase() == "true"){
            lblFeedback.html("This artist already exists");
        }
        else {
            ajaxDataProvider.updateArtist(id, name, function (result) {
                alert("updated");
                window.location.replace(hostUrl + "/artists/");
            });
        }
    });
};