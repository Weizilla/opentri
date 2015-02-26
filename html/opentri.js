$(document).ready(function() {
    $(".dayLong").hide();
    
    if (! window.matchMedia('screen and (min-width: 64em)').matches) {
        $(".weekDays").hide();
    }

    $(".dayLong, .dayShort").click(function() {
        var target = $(this).parent().attr("id");
        $("#" + target + " .dayShort").toggleClass("dayShortSelected");   
        $("#" + target + " .dayLong").toggle();   
    });

    $(".weekToggle").click(function(e) {
        var week = $(this).closest(".week").attr("id");
        var display = $(this).attr("data-display") === "true";
        $("#" + week + " .weekDays").toggle(display);
        e.preventDefault();
    });

    $(".daysToggle").click(function(e) {
        var week = $(this).closest(".week").attr("id");
        var display = $(this).attr("data-display") === "true";
        if (display) {
            $("#" + week + " .weekDays").toggle(display);
        }
        $("#" + week + " .dayShort").toggleClass("dayShortSelected", display);
        $("#" + week + " .dayLong").toggle(display);
        e.preventDefault();
    });
});
