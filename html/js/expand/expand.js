app.controller("ExpandController", ["$routeParams", "$location", "reader", "scroll",
    function($routeParams, $location, reader, scroll) {
        var ctrl = this;
        ctrl.day = {};
        scroll.disable();

        reader.success(function(data) {
            ctrl.day = data[$routeParams.weekIndex].days[$routeParams.dayIndex];
        });

        ctrl.home = function() {
            $location.path("/");
            scroll.enable();
        };
}]);