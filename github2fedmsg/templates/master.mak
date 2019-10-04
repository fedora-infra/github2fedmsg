<!DOCTYPE html>
<html lang="en">
  <head>
    <title>github2fedmsg - rebroadcast GitHub events to the fedmsg bus</title>

    <script type="text/javascript"
      src="${request.static_url('github2fedmsg:static/jquery-1.11.0.min.js')}" ></script>
    <link rel="stylesheet" type="text/css" media="all"
        href="${request.static_url('github2fedmsg:static/bootstrap-3.1.1-fedora/css/bootstrap.min.css')}"/>
    <link rel="stylesheet" type="text/css" media="all"
        href="${request.static_url('github2fedmsg:static/github2fedmsg.css')}"/>

    <script type="text/javascript"
      src="${request.static_url('github2fedmsg:static/messenger-1.4.1/js/messenger.min.js')}" ></script>
    <script type="text/javascript"
      src="${request.static_url('github2fedmsg:static/messenger-1.4.1/js/messenger-theme-flat.js')}" ></script>
    <link rel="stylesheet" type="text/css" media="all"
        href="${request.static_url('github2fedmsg:static/messenger-1.4.1/css/messenger.css')}"/>
    <link rel="stylesheet" type="text/css" media="all"
        href="${request.static_url('github2fedmsg:static/messenger-1.4.1/css/messenger-theme-flat.css')}"/>
  </head>
  <body>
    <div id="wrap" class="container container-fluid">
      ${self.body()}
    </div>

    <div id="footer">
      <div class="container">
        <p class="text-muted credit">
        github2fedmsg is licensed under the
        <a href="http://www.gnu.org/licenses/agpl-3.0.txt">AGPL</a>; the source
        code can be found
        <a href="http://github.com/fedora-infra/github2fedmsg">on github.</a>
        ©2014 Red Hat, Inc., and contributors.
      </div>
    </div>
  </body>
</html>
