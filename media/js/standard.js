$(document).ready(function() {

    $(document).everyTime(2000, function() { 
        update_info();
    });

    // Send the player a command without caring about the return value
    $(".action > p a").click(function(e) {
        // Disable the default behaviors of all our action links         
        e.preventDefault();

        // Get the url from this object
        var target_url = $(this).attr("href");

        // Send Request (and don't wait for a response)
        // The post data sent (source = "ajax") will tell
        // the Django view to not even bother rendering a
        // return page
        $.post(target_url, {source: "ajax"});

        update_info();

    });
});

function update_info() {

    // Get current player info
    $.post('/info/', function(xml) {
        // format and output result
        
        // Get song name
        $("#current_title").html(
            $("current_song title", xml).text());

        // Get song artist
        $("#current_artist").html(
            $("current_song artist", xml).text());

        // Get song album
        $("#current_album").html(
            $("current_song album", xml).text());

        // Get xmms2 status (whether it's playing or not)
        $("#current_status").html(
            $("player_status current_action", xml).text());

        // Decide whether to display the play button or the pause button
        var is_playing_string = $("player_status is_playing", xml).text();
        var is_playing = string_to_boolean(is_playing_string);

        if(is_playing) {
            $("#xmms_play").addClass("hidden");
            $("#xmms_pause").removeClass("hidden");
        } else {
            $("#xmms_play").removeClass("hidden");
            $("#xmms_pause").addClass("hidden");
        }

        // Load in data from playlist
            
        $(xml).find("song").each(function() {
                var position = $(this).attr('id');
                var title = $(this).find('title').text();
                var artist = $(this).find('artist').text();
                var album = $(this).find('album').text();
                $('<div class="playlist_item"></div>').html(
                    '<span class="playlist_item_position">' + position + '</span>' +
                    '<span class="playlist_item_title">' + title + '</span>' +
                    '<span class="playlist_item_artist">' + artist + '</span>' +
                    '<span class="playlist_item_album">' + album + '</span>').appendTo("#playlist");
        });
        
        
    });
}

function string_to_boolean(boolean_string) {
    boolean_string = trim(boolean_string);
    if(boolean_string.toLowerCase() == "true")
    {
        return true;
    }
    else
    {
        return false;
    }
}

function trim(stringToTrim) { 
    return stringToTrim.replace(/^\s+|\s+$/g,"");
}
