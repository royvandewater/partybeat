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

        // We'll want to force a player status update after 500 milliseconds
        // because switching tracks takes a second

        setTimeout("force_update()", 100); 

        update_info();

    });

    $("#playlist > div span a").live("click", function(e) {
        e.preventDefault();
        var target_url = $(this).attr("href");
        $.post(target_url, {source: "ajax"});

        force_update();
    });

});

function force_update() {
        var target_url = "/refresh/";
        $.post(target_url, {source: "ajax"});
}

function update_info() {

    // Get current player info
    $.post('/info/', function(xml) {
        // format and output result
        
        var current_xmms_id = $("current_song xmms_id", xml).text();

        // Get song name 
        $("#current_name").html(
            $("current_song name", xml).text());


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
        target_url = "/playlist/";
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
