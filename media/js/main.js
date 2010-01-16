$(document).ready(function() {
    $(".player_element").corner();
    $("#theme_roller").themeswitcher();

    $("#theme_dialog").dialog({
        title: "Theme Switcher",
        width: 210,
        minHeight: 100,
        height: 100,
        autoOpen: false,
        closeOnEscape: true,
    });

    $("#theme_roll_link").click(function(e) {
        $("#theme_dialog").dialog("open");
    });
});
