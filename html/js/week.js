app.directive("week", ["visibility", function(visibility) {
    return {
        restrict: "E",
        scope: {
            week: "="
        },
        templateUrl: "partials/week.html",
        link: function(scope) {
            scope.show = visibility.show;
            scope.hide = visibility.hide;
            scope.isVisible = visibility.isVisible;
            scope.showDays = visibility.showDays;
            scope.hideDays = visibility.hideDays;
        }
    }
}]);
