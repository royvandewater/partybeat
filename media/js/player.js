// Percentage of the progress bar that is increased each 100 ms
var progress_modifier = 0.0;
// Percentage of the song we have progressed to
var current_progress = 0.0;
var is_playing = false;
var seek_is_dragging = false;
var max_seek = 100;
var timeout = 2000;

$(document).ready(function() {

    update_info();

    // Initialize the slider
    $("#xmms_seek").slider({
        animate: true,
        start: function(event, ui){
            seek_is_dragging = true;
        },
        stop: function(event, ui){
            var new_position = Math.floor(ui.value * max_seek / 100);
            var url = "/player/action/seek/" + new_position + "/";
            $.post(url, {source: "ajax"});
            setTimeout("start_slider()", 2000); 
            update_info();
        },
    });

    $(document).everyTime(timeout, update_info);

    $(document).everyTime(100, function() {
        if( is_playing )
            current_progress += progress_modifier;
        interpolate_progress_bar();
    });


    // Send the player a command without caring about the return value
    $("#xmms_actions > a").click(function(e) {
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
    $.getJSON('/player/info/', function(json) {
            
        // format and output result
        var current_song = json.xmms2.current_song;
        var player_status = json.xmms2.player_status;
        var playlist = json.xmms2.playlist;

        var current_xmms_id = current_song.xmms_id;

        var current_info = current_song.name + " - " + current_song.artist + " - " + current_song.album;

        // Set info
        $("#current_info").html(current_info);
        document.title = "Partybeat - " + current_info.replace("#39;", "'");

        // Get progress on current track
        var seek = player_status.seek;
        max_seek = player_status.max_seek;
        progress_modifier = (100 / max_seek);
        current_progress = seek / max_seek;
        var offset = current_progress * 500;

        // // Decide whether xmms2 is playing (used to determine progress bar interpolation)
        var is_playing_string = player_status.is_playing
        is_playing = string_to_boolean(is_playing_string);

        // Clear the playlist
        $("#playlist_songs").html("");
            
        // Build the playlist
        $.each(playlist, function(i, item) {
            var song_str = item.position + ": " + item.name + " - " + item.artist;

            var hover = ""
            if( item.position == current_song.position )
                hover = " ui-state-hover";

            var html_str = '<div class="playlist_item' + hover + '">' + 
            '<span class="playlist_item_delete">' + 
                '<a href="/player/delete/' + item.position + '/" ' +
                   'class="ui-icon ui-icon-closethick"></a>' + 
            '</span>' + song_str + '</div>';
            $("#playlist_songs").append(html_str);
        });
        
    });
}

function interpolate_progress_bar() {
    var offset = current_progress * 100;
    if(offset < 100 && !seek_is_dragging)
        $("#xmms_seek").slider('value', offset);
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

function start_slider() {
    seek_is_dragging = false;
}
