function subscribe(link) {
    $.ajax(link, {
        success: function(json, stat, xhr) {
            var name, sel;
            name = json.repo.name;
            name = name.replace(/\./g, '\\.');
            sel = $("#"+json.github_username+'-'+name);
            sel.toggleClass('btn-success');
            sel.toggleClass('btn-default');

            if (json.repo.enabled) {
                sel.html("On");
            } else {
                sel.html("Off");
            }
        },
        error: function(json, stat, xhr) {
            console.log('error');
            console.log(json);
        },
    });
}
