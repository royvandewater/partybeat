$(document).ready(function() {

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
    // $("#library_header > a").fancybox(fancybox_settings);
});
