$(document).ready(function() {

    $("#theme_roller").themeswitcher();
    $("#theme_roller_link").click( function(e) {
        e.preventDefault();
        console.log("check");
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
});
