$(document).ready(function() {

    $("#dialog_box").dialog({
        width: 600,
        autoOpen: false,
        closeOnEscape: true,
        modal: true,
    });

    $(".library_row").live('mouseover', function(e) {
            $(this).addClass("ui-state-active");
    });

    $(".library_row").live('mouseout', function(e) {
            $(this).removeClass("ui-state-active");
    });

    $(".song_item").live('click', function(e) {
            var target_url = $(this).find(".library_item_add > a").attr("href");
            $.post(target_url, {source: "ajax"});
            setTimeout("update_info()", 200); 
    });

    $("#search_submit").hide();
    $("#search_input").bind( 'change keyup', function(e){

            if(this.value.length == 0)
            {
                $.getJSON('/library/artists/', function(json) {
                    $("#library_items").html("")
                    $.each(json, function(i, artist) {
                        var li = '<li class="library_item">' + 
                                    '<div class="library_row artist_item">' +
                                    '<div class="ui-icon ui-icon-triangle-1-e" ></div>' +
                                        '<span>' + artist + '</span>' +
                                    '</div>' +
                                  '</li>';
                        $("#library_items").append(li);
                    });
                });
            } else 
            {
                $.getJSON('/library/search/', {search_input: this.value}, function(json) {
                    $("#library_items").html("")
                    
                    var subtree = "";
                    $.each(json, function(i, song) {
                        var id = song.pk;
                        var name = song.fields.name;
                        var artist = song.fields.artist;
                        var album = song.fields.album;
                        var li = '<li>' +
                                    '<div class="library_row song_item">' +
                                        '<span class="library_item_add">' +
                                            '<a href="/library/add/' + id + '/" title="Add to playlist" class="ui-icon ui-icon-plusthick"></a>' +
                                        '</span>' +
                                        '<span class="library_item_edit">' +
                                            '<a href="/library/edit/' + id + '/" title="Edit Song" class="ui-icon ui-icon-gear"></a>' +
                                        '</span>' +
                                        '<span class="library_item_download">' +
                                            '<a href="/library/download/' + id + '/" title="Download Song" class="ui-icon ui-icon-arrowthick-1-s"></a>' +
                                        '</span>' +
                                        '<div class="library_item_details">' + name + ' - ' + artist + ' - ' + album +  '</div>' +
                                        '<div class="clearboth"></div>' +
                                    '</div>' +
                                 '</li>';
                         subtree += li;
                    });

                    // subtree += "</ul>";
                    $("#library_items").append(subtree);
                });
            }
    });
    


    $(".library_item_edit a").live('click', render_popup);
    $("#library_upload a").click(render_popup);

    // Library treeview
    $(".artist_item").live('click', function(e){
        if( !has_childs(this) )
        {
            var artist = $(this).find("> span").html().toLowerCase().replace(/ /g,"_");
            var artist_item = $(this);

            $.getJSON('/library/albums/?artist=' + escape(artist), function(json) {
                var subtree = '<ul class="library_item collapsable library_albums">';
                $.each(json, function(i, album) {
                    var li = '<li>' +
                                 '<div class="library_row album_item">' +
                                     '<div class="ui-icon ui-icon-triangle-1-e" ></div>' +
                                     '<span>' + album  + '</span>' +
                                 '</div>' + 
                             '</li>';
                    subtree += li;
                });

                subtree += "</ul>";
                artist_item.parent().append(subtree);
                artist_item.find("div").removeClass("ui-icon-triangle-1-e");
                artist_item.find("div").addClass("ui-icon-triangle-1-se");
            });
        } else {
            if($(this).find("div.ui-icon").is(".ui-icon-triangle-1-se"))
            {
                $(this).find("div.ui-icon-triangle-1-se").addClass("ui-icon-triangle-1-e");
                $(this).find("div.ui-icon-triangle-1-se").removeClass("ui-icon-triangle-1-se");
            }
            else
            {
                $(this).find("div.ui-icon-triangle-1-e").addClass("ui-icon-triangle-1-se");
                $(this).find("div.ui-icon-triangle-1-e").removeClass("ui-icon-triangle-1-e");
            }
            $(this).parent().find("ul").slideToggle();
        }
    });

    $(".album_item").live('click', function(e){
            if( !has_childs(this) )
            {
                var artist = $(this).parent().parent().parent().find("> div span").html().toLowerCase().replace(/ /g,"_"); 
                var album = $(this).find("> span").html().toLowerCase().replace(/ /g,"_");
                var album_item = $(this);

                $.getJSON('/library/songs/?artist=' + escape(artist) + '&album=' + escape(album), function(json) {
                    var subtree = '<ul class="library_item library_songs">';
                    $.each(json, function(i, song) {
                        var id = song.pk;
                        var name = song.fields.name;
                        var li = '<li>' +
                                    '<div class="library_row song_item">' +
                                        '<span class="library_item_add">' +
                                            '<a href="/library/add/' + id + '/" title="Add to playlist" class="ui-icon ui-icon-plusthick"></a>' +
                                        '</span>' +
                                        '<span class="library_item_edit">' +
                                            '<a href="/library/edit/' + id + '/" title="Edit Song" class="ui-icon ui-icon-gear"></a>' +
                                        '</span>' +
                                        '<span class="library_item_download">' +
                                            '<a href="/library/download/' + id + '/" title="Download Song" class="ui-icon ui-icon-arrowthick-1-s"></a>' +
                                        '</span>' +
                                        '<div class="library_item_details">' + name +  '</div>' +
                                        '<div class="clearboth"></div>' +
                                    '</div>' +
                                 '</li>';
                         subtree += li;
                    });

                    subtree += "</ul>";
                    album_item.parent().append(subtree);
                    album_item.find("div").removeClass("ui-icon-triangle-1-e");
                    album_item.find("div").addClass("ui-icon-triangle-1-se");
                });
            } else {
                if($(this).find("div.ui-icon").is(".ui-icon-triangle-1-se"))
                {
                    $(this).find("div.ui-icon-triangle-1-se").addClass("ui-icon-triangle-1-e");
                    $(this).find("div.ui-icon-triangle-1-se").removeClass("ui-icon-triangle-1-se");
                }
                else
                {
                    $(this).find("div.ui-icon-triangle-1-e").addClass("ui-icon-triangle-1-se");
                    $(this).find("div.ui-icon-triangle-1-e").removeClass("ui-icon-triangle-1-e");
                }
                $(this).parent().find("ul").slideToggle();
            }
    });

});

function has_childs(element) {
    if ($(element).parent().find("ul").length > 0)
        return true;
    else
        return false;
}

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
