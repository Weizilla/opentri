app.directive("day", ["visibility", "$location", "scroll",
    function(visibility, $location, scroll) {
        return {
            restrict: "E",
            scope: {
                day: "="
            },
            templateUrl: "partials/day.html",
            link: function(scope) {
                scope.toggle = visibility.toggle;
                scope.isVisible = visibility.isVisible;
                scope.expand = function(day) {
                    $location.path("/" + day.weekIndex + "/" + day.dayIndex);
                    scroll.disable();
                };
            }
        };
    }]);
