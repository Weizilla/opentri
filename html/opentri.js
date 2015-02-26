function getWeekStart(week) {
    var parts = week.attr("data-weekStart").split("-");
    return new Date(parts[0], parts[1] - 1, parts[2]);
};

$(document).ready(function() {
    $(".dayLong").hide();

    if (! window.matchMedia('screen and (min-width: 64em)').matches) {
        $(".weekDays").hide();
    }

    var today = new Date();
    var lastWeek = new Date();
    lastWeek.setDate(lastWeek.getDate() - 7);
    $(".week").each(function() {
        var thisWeek = $(this);
        var weekStart = getWeekStart(thisWeek);
        if (weekStart < lastWeek) {
            $("#past").append(thisWeek);
        } else if (weekStart < today) {
            thisWeek.find(".weekDays").show();
        }
    });

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
