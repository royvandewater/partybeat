$(document).ready(function() {

    // Send the player a command without caring about the return value
    $(".action > p a").click(function(e) {
        // Disable the default behaviors of all our action links         
        e.preventDefault();

        // Get the url from this object
        var target_url = $(this).attr("href");

        // Send Request (and don't wait for a response)
        $.post(target_url);

        // Get current player info
        $.post('/info/', function(xml) {
            // format and output result
            
            // Get song name
            $("#current_song").html(
                $("current_song name", xml).text()
            )

            // Get song artist
            $("#current_artist").html(
                $("current_song artist", xml).text()
            )

            // Get song album
            $("#current_album").html(
                $("current_song album", xml).text()
            )

            // Decide whether to display the play button or the pause button
            var is_playing_string = $("player_status", xml).text();
            var is_playing = string_to_boolean(is_playing_string);

            if(is_playing) {
                $("#xmms_play").addClass("hidden");
                $("#xmms_pause").removeClass("hidden");
            } else {
                $("#xmms_play").removeClass("hidden");
                $("#xmms_pause").addClass("hidden");
            }
            
        });
    });
});

function string_to_boolean(boolean_string) {
    boolean_string = trim(boolean_string);
    if(boolean_string.toLowerCase() == "true")
        return true;
    else
        return false;
}

function trim(stringToTrim) { 
    return stringToTrim.replace(/^\s+|\s+$/g,"");
}
