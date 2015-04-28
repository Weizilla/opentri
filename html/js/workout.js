app.controller("WorkoutController", ["$window", "reader", "visibility",
    function($window, reader, visibility) {
    var vm = this;
    vm.workouts = [];
    vm.past = [];

    reader.success(function(data){
        var today = new Date();
        var lastWeek = new Date();
        lastWeek.setDate(today.getDate() - 7);

        for (var i = 0; i < data.length; i++) {
            var week = data[i];
            if (week.startDate >= lastWeek) {
                vm.workouts.push(week);
                if ($window.innerWidth > 1024 || today > week.startDate) {
                    visibility.show(week.id);
                }
            } else {
                vm.past.push(week);
            }
        }
    });
}]);