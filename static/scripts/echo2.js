var urlServer = "http://localhost:12345/server"

$(window).load(function () {
    Init();
});


function Init() {

}


$(document).on('click', '#btnGetAnswer', function () {
    ajaxDataProvider.getSimpleAnswer(function (result) {
        $( "#divFeedback" ).append( "<p>" + result.result + "</p>" );
    });
});


$(document).on('click', '#btnClear', function () {
    ajaxDataProvider.getSimpleAnswer(function (result) {
        $( "#divFeedback" ).html( "" );
    });
});