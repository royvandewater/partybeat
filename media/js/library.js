$(document).ready(function() {

    load_artists();

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

    var fancybox_settings = {
        'frameWidth': 450,
        'frameHeight': 180,
        'overlayOpacity': 0.6,
        'hideOnContentClick': false,
    };

    $(".library_item_edit > a").fancybox(fancybox_settings);
    // Uncomment for ajax upload
    $("#library_upload a").fancybox(fancybox_settings);

    $(".library_item").corner('4px');

    
    $("#library_header").click(function(e) {
        load_artists();
    });

    $("#library_items .library_item_artist").live("click", function(e) {
        var artist = urlize($(this).text());
        load_albums(artist);
    });

    $("#library_items .library_item_album").live("click", function(e) {
        var artist = urlize($("#library_current_view h3").text());
        var album = urlize($(this).text());
        load_songs(artist, album);
    });
    
});

function load_artists() {
    // First load the relevant data
    var count = 0;
    $.getJSON('/library/artists/', function(json) {
        $("#library_current_view h3").html("Artists");
        $("#library_items").html("");
        $.each(json.artists, function(i, item) {
            var item_string = '<div class="library_item"><span class="library_item_artist">' + item + '</span></div>';
            $("#library_items").append(item_string);
        });
    });
}

function load_albums(artist) {
    var url = "/library/albums/" + artist + "/";
    $.getJSON(url, function(json) {
        $("#library_current_view h3").html(titleize(artist));
        $("#library_items").html("");
        $.each(json.albums, function(i, item) {
            var item_string = '<div class="library_item"><span class="library_item_album">' + item + '</span></div>';
            $("#library_items").append(item_string);
        });
    });
}

function load_songs(artist, album) {
    var url = "/library/songs/" + artist + "/" + album + "/";
    $.getJSON(url, function(json) {
        $("#library_current_view h3").html(titleize(artist) + " - " + titleize(album));
        $("#library_items").html("");
        $.each(json.songs, function(i, item) {
            var item_string = '<div class="library_item"><span class="library_item_name">' + item + '</span></div>';
            $("#library_items").append(item_string);
        });
    });
}

function titleize(str) {
    return str.replace(/_/g, " ");
}

function urlize(str) {
    return str.replace(/\s/g, "_");
}
