var app = angular.module("opentri", []);

app.controller("WorkoutsController", function(WorkoutsFactory) {
    var vm = this;
    var visible = new Set();

    vm.toggleDay = function(id) {
        if (visible.has(id)) {
            visible.delete(id);
        } else {
            visible.add(id);
        }
        return vm.isDayVisible(id);
    };
    vm.isDayVisible = function(id) {
        return visible.has(id);
    };

    vm.toggleWeek = function(id) {
        return vm.toggleDay("week-" + id);    
    };
    vm.isWeekVisible = function(id) {
        return vm.isDayVisible("week-" + id);
    };

    vm.showAllDays = function(weekId) {
        visible.add("week-" + weekId);
        for (i = 1; i <= 7; i++) {
            visible.add(weekId + "-" + i);
        }
    };

    vm.hideAllDays = function(weekId) {
        for (i = 1; i <= 7; i++) {
            visible.delete(weekId + "-" + i);
        }
    };
    
    vm.workouts = [];
    WorkoutsFactory.getWorkouts().success(function(data) {
        vm.workouts = data;
    });
});

app.factory("WorkoutsFactory", function($http) {
    return {
        getWorkouts: function() {
             return $http.get("/workouts.json");
        }
    };
});
