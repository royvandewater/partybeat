$(document).ready(function() {

    $("#theme_roller").themeswitcher();
    $("#theme_roller_link").click( function(e) {
        e.preventDefault();
        $("#theme_roller").slideToggle();
    });

    $("#popout_library_link").click( function(e) {
        e.preventDefault();
        var windowFeatures = 'height=' + 650 +
                             ',width=' + 850 +
                             ',toolbar=' + 0 +
                             ',scrollbars=' + 1 +
                             ',status=' + 0 + 
                             ',resizable=' + 1 +
                             ',location=' + 0 +
                             ',menuBar=' + 0;

        var library = window.open("/library/", "Library", windowFeatures);
        library.focus(); 
        $("#song_library").fadeOut();
    });

    $("#float_playlist_link").click(popout_playlist);
    $("#float_library_link").click(popout_library);
});

function popout_playlist(e) {
    e.preventDefault();
    popout("#playlist");
}

function popout_library(e) {
    e.preventDefault();
    popout("#song_library");
}

function popout(element) {
    var dialog_options = {
        width: 800,
        autoOpen: true,
        closeOnEscape: false,
        modal: false,
    };

    $(element).dialog(dialog_options);
}
