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

        // We'll want to force a player status update after 200 milliseconds
        // because the daemon needs time to write to the db
        setTimeout("update_info()", 200); 
    });

    $("#playlist > div span a").live("click", function(e) {
        e.preventDefault();
        var target_url = $(this).attr("href");
        $.post(target_url, {source: "ajax"});
    });

});

function update_info() {

    // Get current player info
    $.post('/player/info/', function(xml) {
        // format and output result
        
        var current_xmms_id = $("current_song xmms_id", xml).text();

        var song_name = $("current_song name", xml).text();
        var song_artist = $("current_song artist", xml).text();
        var song_album = $("current_song album", xml).text();

        var current_info = song_name + " - " + song_artist + " - " + song_album;

        // Get info
        $("#current_info").html(current_info);

        // Get xmms2 status (whether it's playing or not)
        $("#current_status").html(
            $("player_status current_action", xml).text());

        // Get progress on current track
        var seek = $("player_status seek");
        var max_seek = $("player_status max_seek");

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
        target_url = "/player/playlist/";
        $("#playlist").load(target_url);
        
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
