<%inherit file="master.mak"/>

<div class="container marketing masthead">
  <h1>github2fedmsg
  <img class="logo" src="${request.static_url('github2fedmsg:static/github2fedmsg.png')}"/>
  </h1>
  <p class="lead">Have stuff on github?  We'll put it on the <a
    href="http://fedmsg.com">fedmsg</a> bus.
  </p>
  %if not request.user:
  <a href="${request.route_url('velruse.openid-url')}" class="btn btn-default btn-lg">
    <span class="glyphicon glyphicon-log-in"></span>
    Sign in with FAS
  </a>
  %endif
</div>
