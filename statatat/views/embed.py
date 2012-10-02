""" Contains code for producing embeddable widgets """

from pyramid.view import view_config

import tw2.core.core
from moksha.wsgi.widgets.api import get_moksha_socket
import BeautifulSoup


# Embedding the widget in an iframe is easy
@view_config(context="tw2.core.widgets.WidgetMeta",
             name='iframe',
             renderer='iframe.mak')
@view_config(context="tw2.core.widgets.WidgetMeta",
             renderer='widget.mak')
def widget_view(request):
    return dict(widget=request.context)


# Embedding the widget as a self-extracting script is a
# little more difficult :D
js_helpers = """
function include_js(url, success) {
    var script     = document.createElement('script');
    script.src = url;

    var head = document.getElementsByTagName('head')[0],
    done = false;
    // Attach handlers for all browsers
    script.onload = script.onreadystatechange = function() {
        if (!done && (
                !this.readyState ||
                this.readyState == 'loaded' ||
                this.readyState == 'complete'
                )) {
            done = true;
            success();  // Do the callback
            script.onload = script.onreadystatechange = null;
            head.removeChild(script);
        };
    };
    head.appendChild(script);
};

function run_with_jquery(callback) {
    var jq_url = 'http://ajax.googleapis.com/ajax/libs' + \
            '/jquery/1.4.4/jquery.min.js';
    if (typeof jQuery == 'undefined') {
        include_js(jq_url, callback);
    } else {
        callback();
    }
}"""


@view_config(context="tw2.core.widgets.WidgetMeta",
             name='javascript',
             renderer='string')
def widget_view_javascript(request):
    """ This code is super ugly.

    But it produces a widget as a self-extracting script.
    """

    # TODO -- get this from the pyramid config
    prefix = "http://localhost:6543"

    raw_widget = request.context.display()
    socket = get_moksha_socket(request.registry.settings).display()
    socket = '\n'.join(socket.strip().split('\n')[1:-1])
    resources = tw2.core.core.request_local().pop('resources', [])
    scripts, calls = [], [socket]
    for r in resources:
        if getattr(r, 'link', None):
            if any(map(r.link.endswith, ['jquery.js', '.css'])):
                continue
            scripts.append(r.link)
        else:
            calls.append(str(r))

    calls.insert(0, "$('body').append('%s')" % raw_widget.strip())
    # Just for debugging...
    #calls.append("console.log('waaaaaat!');")
    inner_payload = ";\n".join(calls)

    envelope = inner_payload
    for script in reversed(scripts):
        envelope = """$.getScript("%s", function(){%s});""" % (
            prefix + script, envelope)

    return js_helpers + "\nrun_with_jquery(function() {%s});" % envelope
