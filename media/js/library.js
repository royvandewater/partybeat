$(document).ready(function() {

    $("#dialog_box").dialog({
        width: 600,
        autoOpen: false,
        closeOnEscape: true,
        modal: true,
    });

    $(".library_item").hover(
        function(e) {
            $(this).addClass("ui-state-active");
        },
        function(e) {
            $(this).removeClass("ui-state-active");
        });

    $(".library_item_add > a").click(function(e) {
        // Disable the default click behaviour
        e.preventDefault();

        // Get this object's url
        var target_url = $(this).attr("href");
        
        // Send Request (and don't wait for a response)
        $.post(target_url, {source: "ajax"});


        // Update info is from player.js, forces the playlist to update
        setTimeout("update_info()", 200); 
    });

    $(".library_item_details").click(function(e) {
            var target_url = $(this).parent().find(".library_item_add > a").attr("href");
            $.post(target_url, {source: "ajax"});
    });


    $(".library_item_edit a").click(render_popup);
    $("#library_upload a").click(render_popup);


    // $("#theme_roll_link").click(render_theme_roller);
});

function render_popup(e) {
        e.preventDefault();

        var target_url = $(this).attr("href");
        var title = $(this).attr("title");

        $.post(target_url, {source: "ajax"}, function(e){
            $("#dialog_box").html(e);
        });

        $("#dialog_box").dialog('open');
        $("#dialog_box").dialog('option', 'title', title);
}

// function render_theme_roller(e) {
        // $("#theme_dialog").dialog({
            // title: "Theme Switcher",
            // width: 210,
            // minHeight: 100,
            // height: 100,
            // autoOpen: false,
            // closeOnEscape: true,
        // });
        // e.preventDefault();

        // var target_url = $(this).attr("href");
        // var title = $(this).attr("title");

        // var roller_div = '<div id="theme_roller"></div>';
        // $("#dialog_box").html(roller_div);

        // $("#dialog_box").dialog('open');
        // $("#dialog_box").dialog('option', 'title', title);
        // $("#theme_roller").themeswitcher();
// }
