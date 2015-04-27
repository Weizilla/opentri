app.filter("join", function () {
    return function (items) {
        return items.length > 0 ? items.join("<br/>") : "&nbsp;";
    };
});

app.filter("sanitize", function ($sce) {
    return function (htmlCode) {
        return $sce.trustAsHtml(htmlCode);
    };
});