var ajaxDataProvider = {
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
    },

    ifArtistExist: function (name, callback) {
        $.ajax({
            type: "GET",
            url: urlServer,
            data: {
                f: 'ifArtistExist',
                name: name,
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
    },

    insertArtist: function (name, callback) {
        $.ajax({
            type: "GET",
            url: urlServer,
            data: {
                f: 'insertArtist',
                name: name,
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
    },

    deleteArtist: function (id, callback) {
        $.ajax({
            type: "GET",
            url: urlServer,
            data: {
                f: 'deleteArtist',
                id: id,
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
    },

    updateArtist: function (id, name, callback) {
        $.ajax({
            type: "GET",
            url: urlServer,
            data: {
                f: 'updateArtist',
                id: id,
                name: name
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
};