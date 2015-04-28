var app = angular.module("OpenTriApp", ["ngRoute"]);

app.config(function($routeProvider) {
    $routeProvider
        .when("/", { })
        .when("/:weekIndex/:dayIndex", {
            controller: "ExpandController",
            controllerAs: "ctrl",
            templateUrl: "partials/expand.html"
        })
        .otherwise({
            redirectTo: "/"
        })
});