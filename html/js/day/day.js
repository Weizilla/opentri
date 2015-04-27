app.directive("day", function(){
    return {
        restrict: "E",
        scope: {
            day: "="
        },
        templateUrl: "js/day/day.html"
    };
});

