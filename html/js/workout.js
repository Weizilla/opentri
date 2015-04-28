app.controller("WorkoutController", ["reader", "visibility",
    function(reader, visibility) {
    var vm = this;
    vm.workouts = [];
    vm.past = [];

    reader.success(function(data){
        var today = new Date();
        var lastWeek = new Date();
        lastWeek.setDate(today.getDate() - 7);

        for (var i = 0; i < data.length; i++) {
            var week = data[i];
            if (week.startDate < lastWeek) {
                vm.past.push(week);
            } else {
                vm.workouts.push(week);
                visibility.show(week.id);
            }
        }
    });
}]);