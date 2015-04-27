app.directive("day", ["visibility", function(visibility) {
    return {
        restrict: "E",
        scope: {
            day: "="
        },
        templateUrl: "js/day/day.html",
        link: function(scope) {
            scope.toggle = visibility.toggle;
            scope.isVisible = visibility.isVisible;
        }
    };
}]);
