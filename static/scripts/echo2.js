var urlServer = "http://localhost:12345/server"

$(window).load(function () {
    Init();
});


function Init() {

}


$(document).on('click', '#btnGetAnswer', function () {
    aDataProvider.getSimpleAnswer(function (result) {
        //alert("OK");
        //alert(result);
        $( "#divFeedback" ).append( "<p>" + result.result + "</p>" );
    });
});


$(document).on('click', '#btnClear', function () {
    aDataProvider.getSimpleAnswer(function (result) {
        $( "#divFeedback" ).html( "" );
    });
});






var aDataProvider = {
    getSimpleAnswer: function (callback) {
        $.ajax({
            type: "GET",
            url: urlServer,
            data: {
                f: 'getSimpleAnswer',
            },
            dataType: 'json',
            success: function(result) {
                callback(result);
            },
            error: function(msg) {
                var errorMessage;
                errorMessage = "ERROR\r\n\r\n";
                errorMessage += msg.status + "\r\n";
                errorMessage += msg.statusText + "\r\n";
                errorMessage += msg.responseText + "\r\n";
                errorMessage += msg.errorThrown;
                alert(errorMessage);
            }
        });
    }

}