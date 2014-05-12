# This file is a part of github2fedmsg, a pubsubhubbub to zeromq bridge.
# Copyright (C) 2014, Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" This is just an example fedmsg config file to be used
during development of github2fedmsg.
"""

import socket
hostname = socket.gethostname().split('.')[0]

config = dict(
    endpoints={
        "relay_outbound": ["tcp://127.0.0.1:4001"],
        "github2fedmsg.%s" % hostname: [
            "tcp://127.0.0.1:5001",
            "tcp://127.0.0.1:5002",
            "tcp://127.0.0.1:5003",
        ],
    },

    relay_inbound="tcp://127.0.0.1:2003",
    environment="dev",
    high_water_mark=0,
    io_threads=1,
    post_init_sleep=0.2,
    irc=[],
    zmq_enabled=True,
    zmq_strict=False,

    sign_messages=False,
    validate_messages=False,
)
