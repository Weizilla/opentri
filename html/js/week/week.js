app.directive("week", function() {
    return {
        restrict: "E",
        scope: {
            week: "="
        },
        templateUrl: "js/week/week.html",
        controller: "VisibilityController",
        controllerAs: "ctrl"
    }
});
