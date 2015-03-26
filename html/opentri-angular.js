var app = angular.module("opentri", []);

app.controller("WorkoutsController", function(WorkoutsFactory) {
    var visibles = new Set();
    this.toggle = function(id) {
        if (visibles.has(id)) {
            visibles.delete(id);
        } else {
            visibles.add(id);
        }
    };
    this.isVisible = function(id) {
        return visibles.has(id);
    };
    this.workouts = WorkoutsFactory;
});

app.factory("WorkoutsFactory", function() {
    return [
        {
            weekNum: 1,
            startDate: "2015-1-1",
            weekHeader: "WEEK 1 HEADER HERE",
            weekTotals: {
                swim: "0:30",
                bike: "2:00",
                run: "1:00"
            },
            days: [
                {
                    dayId: "1-1",
                    dayOfWeek: "Monday",
                    dayTotals: {
                        swim: "1:15",
                        bike: "1:30",
                        run: "1:00"
                    },
                    dayWorkout: "DAY 1 REALLY LONG WORKOUT HERE. LOTS OF SWIMMING BIKING RUNNING. SWIM BIKE RUN. SWIM BIKE RUN"
                },
                {
                    dayId: "1-2",
                    dayOfWeek: "Tuesday",
                    dayTotals: {
                        swim: "2:15",
                        bike: "2:30",
                        run: "2:00"
                    },
                    dayWorkout: "DAY 2 REALLY LONG WORKOUT HERE. LOTS OF SWIMMING BIKING RUNNING. SWIM BIKE RUN. SWIM BIKE RUN"
                },
                {
                    dayId: "1-3",
                    dayOfWeek: "Wednesday",
                    dayTotals: {
                        swim: "3:15",
                        bike: "3:30",
                        run: "3:00"
                    },
                    dayWorkout: "DAY 3 REALLY LONG WORKOUT HERE. LOTS OF SWIMMING BIKING RUNNING. SWIM BIKE RUN. SWIM BIKE RUN"
                },
                {
                    dayId: "1-4",
                    dayOfWeek: "Thursday",
                    dayTotals: {
                        swim: "4:15",
                        bike: "4:30",
                        run: "4:00"
                    },
                    dayWorkout: "DAY 4 REALLY LONG WORKOUT HERE. LOTS OF SWIMMING BIKING RUNNING. SWIM BIKE RUN. SWIM BIKE RUN"
                },
                {
                    dayId: "1-5",
                    dayOfWeek: "Friday",
                    dayTotals: {
                        swim: "5:55",
                        bike: "5:30",
                        run: "5:00"
                    },
                    dayWorkout: "DAY 5 REALLY LONG WORKOUT HERE. LOTS OF SWIMMING BIKING RUNNING. SWIM BIKE RUN. SWIM BIKE RUN"
                },
                {
                    dayId: "1-6",
                    dayOfWeek: "Saturday",
                    dayTotals: {
                        swim: "6:65",
                        bike: "6:30",
                        run: "6:00"
                    },
                    dayWorkout: "DAY 6 REALLY LONG WORKOUT HERE. LOTS OF SWIMMING BIKING RUNNING. SWIM BIKE RUN. SWIM BIKE RUN"
                },
                {
                    dayId: "1-7",
                    dayOfWeek: "Sunday",
                    dayTotals: {
                        swim: "7:15",
                        bike: "7:30",
                        run: "7:00"
                    },
                    dayWorkout: "DAY 7 REALLY LONG WORKOUT HERE. LOTS OF SWIMMING BIKING RUNNING. SWIM BIKE RUN. SWIM BIKE RUN"
                },
            ]
        }, {
            weekNum: 2,
            startDate: "2015-2-1",
            weekHeader: "WEEK 2 HEADER HERE",
            weekTotals: {
                swim: "0:30",
                bike: "2:00",
                run: "1:00"
            },
            days: [
                {
                    dayId: "2-1",
                    dayOfWeek: "Monday",
                    dayTotals: {
                        swim: "1:15",
                        bike: "1:30",
                        run: "1:00"
                    },
                    dayWorkout: "DAY 1 REALLY LONG WORKOUT HERE. LOTS OF SWIMMING BIKING RUNNING. SWIM BIKE RUN. SWIM BIKE RUN"
                },
                {
                    dayId: "2-2",
                    dayOfWeek: "Tuesday",
                    dayTotals: {
                        swim: "2:15",
                        bike: "2:30",
                        run: "2:00"
                    },
                    dayWorkout: "DAY 2 REALLY LONG WORKOUT HERE. LOTS OF SWIMMING BIKING RUNNING. SWIM BIKE RUN. SWIM BIKE RUN"
                },
                {
                    dayId: "2-3",
                    dayOfWeek: "Wednesday",
                    dayTotals: {
                        swim: "3:15",
                        bike: "3:30",
                        run: "3:00"
                    },
                    dayWorkout: "DAY 3 REALLY LONG WORKOUT HERE. LOTS OF SWIMMING BIKING RUNNING. SWIM BIKE RUN. SWIM BIKE RUN"
                },
                {
                    dayId: "2-4",
                    dayOfWeek: "Thursday",
                    dayTotals: {
                        swim: "4:15",
                        bike: "4:30",
                        run: "4:00"
                    },
                    dayWorkout: "DAY 4 REALLY LONG WORKOUT HERE. LOTS OF SWIMMING BIKING RUNNING. SWIM BIKE RUN. SWIM BIKE RUN"
                },
                {
                    dayId: "2-5",
                    dayOfWeek: "Friday",
                    dayTotals: {
                        swim: "5:55",
                        bike: "5:30",
                        run: "5:00"
                    },
                    dayWorkout: "DAY 5 REALLY LONG WORKOUT HERE. LOTS OF SWIMMING BIKING RUNNING. SWIM BIKE RUN. SWIM BIKE RUN"
                },
                {
                    dayId: "2-6",
                    dayOfWeek: "Saturday",
                    dayTotals: {
                        swim: "6:65",
                        bike: "6:30",
                        run: "6:00"
                    },
                    dayWorkout: "DAY 6 REALLY LONG WORKOUT HERE. LOTS OF SWIMMING BIKING RUNNING. SWIM BIKE RUN. SWIM BIKE RUN"
                },
                {
                    dayId: "2-7",
                    dayOfWeek: "Sunday",
                    dayTotals: {
                        swim: "7:15",
                        bike: "7:30",
                        run: "7:00"
                    },
                    dayWorkout: "DAY 7 REALLY LONG WORKOUT HERE. LOTS OF SWIMMING BIKING RUNNING. SWIM BIKE RUN. SWIM BIKE RUN"
                },
            ]
        }
    ];
});
