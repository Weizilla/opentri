app.controller("VisibilityController", function() {
    var ctrl = this;
    ctrl.visible = new Set();

    ctrl.isVisible = function(id) {
        return ctrl.visible.has(id);
    };

    ctrl.toggle = function(id) {
        if (ctrl.isVisible(id)) {
            ctrl.hide(id);
        } else {
            ctrl.show(id);
        }
    };

    ctrl.show = function(id) {
        ctrl.visible.add(id);
    };

    ctrl.hide = function(id) {
        ctrl.visible.delete(id);
    };

    ctrl.showDays = function(id) {
        ctrl.show("week-" + id);
        for (var i = 1; i <= 7; i++) {
            ctrl.show("day-" + id + "-" + i)
        }
    };

    ctrl.hideDays = function(id) {
        for (var i = 1; i <= 7; i++) {
            ctrl.hide("day-" + id + "-" + i)
        }
    };
});