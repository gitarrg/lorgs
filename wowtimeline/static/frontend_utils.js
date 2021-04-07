


function refresh_instances() {
    console.log("REFRESH_INSTANCES");

    var icon = $(this).find("i");
    icon.addClass("fa-spin");

    $.get({
        url: "api/instances/refresh",
        success: function() {
            console.log("DONE!");
            icon.removeClass("fa-spin");
            // location.reload(); // sorry :(

            refresh_progress_bar();
        }
    });
}