$(document).ready(function() {

    $("#theme_roller").themeswitcher();
    $("#theme_roller_link").click( function(e) {
        e.preventDefault();
        $("#theme_roller").slideToggle();
    });
});
