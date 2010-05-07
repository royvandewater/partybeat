
// Percentage of the progress bar that is increased each 100 ms
var progress_modifier = 0.0;
// Percentage of the song we have progressed to
var current_progress = 0.0;
var is_playing = false;
var seek_is_dragging = false;
var volume_is_dragging = false;
var max_seek = 100;
var timeout = 2000;
var playlist_hash = "aoneusth";
var last_update = Date.now();
var playlist_sort_order = new Array();

var template_playlist = "\u003C% $.each(playlist, function(i, item) { %\u003E\u000A\u003Cdiv class\u003D\u0022playlist_item\u003C% if( item.position \u003D\u003D current_song.position ) { %\u003E ui\u002Dstate\u002Dhover\u003C% } %\u003E\u0022\u003E\u000A  \u003Cspan class\u003D\u0022playlist_item_delete\u0022\u003E\u000A    \u003Ca href\u003D\u0022/player/delete/\u003C%\u003D item.position %\u003E/\u0022 class\u003D\u0022ui\u002Dicon ui\u002Dicon\u002Dclosethick\u0022\u003E\u003C/a\u003E\u000A  \u003C/span\u003E\u000A  \u003Ca href\u003D\u0022/player/skip_to/\u003C%\u003D item.position %\u003E/\u0022 class\u003D\u0022song_name\u0022\u003E\u000A    \u003C%\u003D item.position %\u003E: \u003C%\u003D item.name %\u003E \u002D \u003C%\u003D item.artist %\u003E\u000A  \u003C/a\u003E\u000A\u003C/div\u003E\u000A\u003C% })\u003B %\u003E\u000A";

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

    $("#xmms_volume").slider({
        animate: true,
        start: function(event, ui){
            volume_is_dragging = true;
        },
        stop: function(event, ui) {
            volume_position = ui.value;
            var url = "/player/volume/" + volume_position + "/";
            $.post(url, {source: "ajax"});
            setTimeout("start_volume()", 2000)
            update_info();
        },
    });

    $("#volume_show").click( function(e) {
        $("#xmms_volume").slideToggle();
    });

    $(document).everyTime(timeout, update_info);

    $(document).everyTime(100, function() {
        if( is_playing && ((current_progress + progress_modifier) > current_progress))
            current_progress += progress_modifier;
        interpolate_progress_bar();
    });


    // Send the player a command without caring about the return value
    $("#xmms_actions > a, #shuffle_playlist_link").click(function(e) {
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

    $("#playlist_songs").sortable({
            stop: function(event, ui) {
                // See what was moved
                
                var item = ui.item.find("span > a").attr("href");

                var old_location = index_of(item, playlist_sort_order);
                var new_location = index_of(item, update_playlist_order());
                var url = "/player/move/" + old_location + "/to/" + new_location + "/";
                if (old_location != new_location) {
                    $.post(url, {source: "ajax"});
                    console.log(url);
                    playlist_sort_order = update_playlist_order();
                }
            }
    });

    //Highlight hovered over row
    $(".playlist_item > .song_name").live("click", function(e) {
        e.preventDefault();
        var target_url = $(this).attr("href");
        $.post(target_url, {source: "ajax"});
        // setTimeout("update_info()", 200); 
    });

    $(".playlist_item > .playlist_item_delete > a").live("click", function(e) {
        e.preventDefault();
        var target_url = $(this).attr("href");
        $.post(target_url, {source: "ajax"});
        $(this).parent().parent().addClass("ui-state-disabled");
        playlist_hash = "cheese";
    });

    $(".playlist_item").live("mouseover", function(e) {
        $(this).addClass("ui-state-active");
    });

    $(".playlist_item").live("mouseout", function(e) {
            $(this).removeClass("ui-state-active");
    });
        
});

function update_info() {
    var call_time = Date.now();
    // Get current player info
    $.getJSON('/player/info/', function(json) {

        if(call_time > last_update) {
            last_update = call_time;

            var player_status = json.xmms2.player_status;
            // Get progress on current track
            var seek = player_status.seek;
            max_seek = player_status.max_seek;
            progress_modifier = (100 / max_seek);
            var new_progress = seek / max_seek;
            if((new_progress > current_progress) || ((current_progress - new_progress) > 0.05))
                current_progress = new_progress;
            var offset = current_progress * 500;

            // Decide whether xmms2 is playing (used to determine progress bar interpolation)
            var is_playing_string = player_status.is_playing;
            is_playing = string_to_boolean(is_playing_string);

            var current_song = json.xmms2.current_song;
            var current_info = current_song.name + " - " + current_song.artist + " - " + current_song.album;
            document.title = "Partybeat - " + current_info;
             
            // Set info
            $("#current_info").html(current_info);

            if(!volume_is_dragging)
                $("#xmms_volume").slider('value', player_status.volume);

            if(playlist_hash != player_status.hash)
            {
                $("#xmms_seek").slider('value', offset);
                // format and output result
                var playlist = json.xmms2.playlist;

                var current_xmms_id = current_song.xmms_id;

                playlist_hash = player_status.hash;

                // Clear the playlist
                // $("#playlist_songs").html("");

                // Build the playlist
                html_string = Jst.evaluateSingleShot(template_playlist, {"playlist":playlist, "current_song":current_song});
                $("#playlist_songs").html(html_string);

                playlist_sort_order = update_playlist_order();
            }
    }
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

function start_volume() {
    volume_is_dragging = false;
}

function update_playlist_order() {
    sort_order = new Array();
    $("#playlist_songs div").each(function(e) {
            sort_order.push($(this).find("span > a").attr("href"));
    });
    return sort_order;
}

function index_of(element, arr) {
    // Finds index of element in array arr
    var i=0;
    for(i=0; i < arr.length; i++)
        if(arr[i] == element)
            return i;
    return -1;
}
