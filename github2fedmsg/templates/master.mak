<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="stylesheet" type="text/css" media="all"
        href="/static/bootstrap-3.0.2-fedora/css/bootstrap.min.css"/>
    <link rel="stylesheet" type="text/css" media="all"
        href="/static/bootstrap-3.0.2-fedora/css/bootstrap-theme.min.css"/>
    <link rel="stylesheet" type="text/css" media="all"
        href="/static/github2fedmsg.css"/>
  </head>
  <body>
    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container container-fluid">
          <a class="brand" href="/">github2fedmsg</a>
          <ul class="nav pull-right">
            <li class="">
            %if request.user:
              <form class="navbar-form pull-right" action="/logout" method="get">
                <input class="btn btn-info" type="submit" value="Sign out" />
              </form>
            %else:
              <form class="navbar-form pull-right" action="/login/openid" method="post">
                <input class="btn btn-primary" type="submit" value="Sign in with FAS" />
              </form>
            %endif
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="vspace"></div>

    <div class="container container-fluid">
      ${self.body()}
    </div>

    <footer class="container container-fluid">
    <p><center>github2fedmsg is written by <a href="http://threebean.org">Ralph Bean</a>
      and is licensed under the
      <a href="http://www.gnu.org/licenses/agpl-3.0.txt">AGPL</a>; the source
      code can be found
      <a href="http://github.com/fedora-infra/github2fedmsg">on github.</a>
      </center></p>
    </footer>

  </body>
</html>
