var getUrl = window.location;
var hostUrl = getUrl.protocol + "//" + getUrl.host;

var lblFeedback = $('#divFeedback');

$(window).load(function () {
    init();
});


function init() {
    lblFeedback = $('#divFeedback')
}


$(document).on('click', '#btnAdd', function () {
    lblFeedback.html("");

    var newName = $('#txtName').val();

    if (newName.length == 0){
        lblFeedback.html("Name must be entered")
    }
    else {
        ifArtistExist(newName);
    }
});


$(document).on('click', '#btnCancel', function () {
    window.location.replace(hostUrl + "/artists/");
});


function ifArtistExist(name){
    ajaxDataProvider.ifArtistExist(name, function (result) {
        if (result.result.toLowerCase() == "true"){
            lblFeedback.html("This artist already exists");
        }
        else {
            ajaxDataProvider.insertArtist(name, function (result) {
                alert("New artist id = " + result.id);
                window.location.replace(hostUrl + "/artists/");
            });
        }
    });
};
