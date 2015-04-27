app.directive("day", function(){
    return {
        restrict: "E",
        scope: {
            day: "="
        },
        templateUrl: "js/day/day.html",
        require: "^week",
        link: function(scope, element, attrs, visCtrl) {
            scope.toggle = function(id) {
                visCtrl.toggle(id);
            };
            scope.isVisible = function(id) {
                return visCtrl.isVisible(id);
            };
        }
    };
});

