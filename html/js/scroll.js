app.factory("scroll", function($document) {
    var scroll = {};
    scroll.enable = function() {
        var bodyRef = angular.element($document[0].body);
        bodyRef.removeClass("noScroll");
    };
    scroll.disable = function() {
        var bodyRef = angular.element($document[0].body);
        bodyRef.addClass("noScroll");
    };
    return scroll;
});