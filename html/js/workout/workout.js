app.controller("WorkoutController", ["reader", function(reader){
    var vm = this;
    vm.workouts = [];

    reader.success(function(data){
        vm.workouts = data;
    });
}]);