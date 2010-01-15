$(document).ready(function() {

    $("#dialog_box").dialog({
        width: 550,
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
