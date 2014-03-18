function subscribe(link) {
    $.ajax(link, {
        success: function(json, stat, xhr) {
            var name, sel;
            name = json.repo.name;
            name = name.replace('.', '\\.');
            sel = $("#"+json.github_username+'-'+name);
            sel.toggleClass('btn-success');
            sel.toggleClass('btn-danger');

            if (json.repo.enabled) {
                sel.html("Disable");
            } else {
                sel.html("Enable");
            }
        },
        error: function(json, stat, xhr) {
            console.log('error');
            console.log(json);
        },
    });
}
