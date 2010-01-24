$(document).ready(function() {

    $("#dialog_box").dialog({
        width: 600,
        autoOpen: false,
        closeOnEscape: true,
        modal: true,
    });

    $(".library_row").hover(
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

    // Library treeview
    $(".artist_item").click(function(e){
        if( $(this).html().length == 0)
        {
            var artist = $(this).parent().find("> span").html().toLowerCase().replace(/ /g,"_");
            var artist_item = $(this);

            $.getJSON('/library/albums/artist/' + artist + '/', function(json) {
                var subtree = '<ul class="library_item collapsable">';
                $.each(json, function(i, album) {
                    var li = '<li>' +
                                 '<div class="library_row"' +
                                     '<div class="ui-icon ui-icon-folder-collapsed album_item" ></div>' +
                                     '<span class="album_item">' + album  + '</span>' +
                                 '</div>' + 
                             '</li>';
                    subtree += li;
                });

                subtree += "</ul>";
                artist_item.parent().parent().append(subtree);
            });
        } else {
            $(this).html("");
        }
    });

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

function display_artists() {
    $('#library_items').html("")
    $.getJSON('/library/artists/', function(json) {
        $.each(json, function(i, artist) {
            $('#library_items').append('<div class="library_item">' + artist + '</div>');
        });
    });
}
