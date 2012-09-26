
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


def make_chart(backend):
    return MessagesTimeSeries(backend=backend)
