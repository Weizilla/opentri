app.directive("weekHeader", ["visibility", function(visibility) {
    return {
        restrict: "E",
        scope: {
            week: "="
        },
        templateUrl: "js/week/header.html",
        link: function(scope) {
            scope.isVisible = function(id) {
                return visibility.isVisible("header-" + id);
            };
            scope.toggle = function(id) {
                visibility.toggle("header-" + id);
            };
        }
    };
}]);