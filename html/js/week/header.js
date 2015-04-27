app.directive("weekHeader", function() {
    return {
        restrict: "E",
        scope: {
            week: "="
        },
        templateUrl: "js/week/header.html"
    };
});