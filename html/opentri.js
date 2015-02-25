$(document).ready(function() {
    $('.dayLong').hide();

    $('.dayShort').click(function() {
        var target = $(this).attr("data-target");
        $("#" + target).toggle();   
    });

    $(".weekToggle").click(function(e) {
        var target = $(this).attr("data-target");
        var display = $(this).attr("data-display") === "true";
        $("." + target).toggle(display);
        e.preventDefault();
    });
});