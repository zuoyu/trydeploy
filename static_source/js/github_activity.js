(function () {

'use strict';

function createActivity(data) {
    var html = '<li>' 
            + data.type + ': ' + data.repo.name
            + '</li>';
    return html;
}

function load() {
    var url = 'https://api.github.com/users/' + github_username + '/events';
    $.get(url, function(data) {
        console.log(data);
        var container = $('#github_activity_container');
        $.each(data, function (index, value) {
            var item = createActivity(value);
            container.append(item);
        }); 
    });
}

$(document).ready(load)

})();