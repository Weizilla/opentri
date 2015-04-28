app.factory("reader", function($http) {
    return $http.get("workouts.json")
        .success(function(data){
            for (var i = 0; i < data.length; i++) {
                data[i].startDate = new Date(data[i].startDate);
            }
            return data;
        })
        .error(function(data){
            return data;
        });
});
