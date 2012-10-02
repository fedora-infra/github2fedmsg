from tw2.jqplugins.gritter import gritter_resources
from tw2.d3 import TimeSeriesChart
from moksha.wsgi.widgets.api.live import LiveWidget

global_width = 960


class MessagesTimeSeries(TimeSeriesChart, LiveWidget):
    id = 'messages-time-series'
    topic = "*"
    onmessage = "tw2.store['${id}'].value++;"

    width = global_width
    height = 75

    # Keep this many data points
    n = 100
    # Initialize to n zeros
    data = [0] * n


def make_chart(backend, topic="*"):
    return MessagesTimeSeries(backend=backend, topic=topic)


class PopupNotification(LiveWidget):
    topic = "login"
    onmessage = """
    (function(json){
        var title = "Login";
        var body = json.username + " just logged in.";
        var image = json.avatar;
        $.gritter.add({'title': title, 'text': body, 'image': image});
    })(json);
    """
    resources = LiveWidget.resources + gritter_resources
    backend = "websocket"

    # Don't actually produce anything when you call .display() on this widget.
    inline_engine_name = "mako"
    template = ""
