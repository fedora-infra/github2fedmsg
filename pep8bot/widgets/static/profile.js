function subscribe(link) {
    $.ajax(link, {
        success: function(json, stat, xhr) {
            var sel = $("#"+json.user+'-'+json.repo.name+'-'+json.kind);
            sel.toggleClass('btn-success');
            sel.toggleClass('btn-danger');

            if (json.repo[json.kind+'_enabled']) {
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
