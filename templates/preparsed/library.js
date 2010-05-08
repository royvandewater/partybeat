var latest_search = Date.now();
var search_field = "";

var template_artists = "{% filter escapejs %}{% include 'library/artists.jst.html' %}{% endfilter %}";
var compiled_artists = Jst.compile(template_artists);

var template_albums = "{% filter escapejs %}{% include 'library/albums.jst.html' %}{% endfilter %}";
var compiled_albums = Jst.compile(template_albums);

var template_songs = "{% filter escapejs %}{% include 'library/songs.jst.html' %}{% endfilter %}";
var compiled_songs = Jst.compile(template_songs);

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


    $(".song_item .library_item_details").live('click', function(e) {
            var target_url = $(this).parent().find(".library_item_add > a").attr("href");
            $.post(target_url, {source: "ajax"});
            setTimeout("update_info()", 1000); 
    });

    $(".hideme .library_item_details").live('click', function(e) {
            $(this).parent().parent().fadeTo(100,.5).fadeTo(100,1);
    });

    $(".library_item_add a, #add_random_link").live('click', function(e) {
            e.preventDefault();
            var target_url = $(this).attr("href");
            $.post(target_url, {source: "ajax"});
            setTimeout("update_info()", 1000); 
    });

    $(".hideme a").live('click', function(e) {
            $(this).parent().parent().parent().fadeTo(100,50).fadeTo(100,100);
    });

    $("#search_submit").hide();
    $("#search_input").bind( 'change keyup', function(e){
            
        if (e.keyCode == 27){
            this.value = "";
        }

        var contents = this.value;
        var search_time = Date.now();
        if(contents != search_field) {
            search_field = contents;
            search(e,contents,search_time);
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
                var subtree = Jst.evaluate(compiled_albums, {"json":json});

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
                    var subtree = Jst.evaluate(compiled_songs, {"json":json});
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

function search(e, value, search_time) {
    // if($("#search_input").attr("value") == value) {
    if(value.length == 0) {
        $.getJSON('/library/artists/', function(json) {
            if(search_time > latest_search) {
                latest_search = search_time;
                var html_string = Jst.evaluate(compiled_artists, {"json":json});
                $("#library_items").html(html_string);
            }
        });
    } else {
        $.getJSON('/library/search/', {search_input: value}, function(json) {
                if (search_time > latest_search) {
                    latest_search = search_time;

                    var subtree = "";
                    $.each(json, function(i, song) {
                        var id = song.pk;
                        var name = song.fields.name;
                        var artist = song.fields.artist;
                        var album = song.fields.album;
                        var li = '<li>' +
                        '<div class="library_row song_item hideme">' +
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
                    var cur_tree = $("#library_items").html();
                    if(cur_tree != subtree) {
                        $("#library_items").html("");
                        $("#library_items").append(subtree);
                    }
                }
        });
    }
}

function show_items() {
    $("#library_items .song_item").fadeIn();
}
