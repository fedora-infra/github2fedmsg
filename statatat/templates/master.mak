<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="stylesheet" type="text/css" href="/static/statatat.css" media="all"/>
  </head>
  <body>
    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="brand" href="./">statatat</a>
          <ul class="nav pull-right">
            <li class="">
            %if request.user:
              <form class="navbar-form" action="/logout" method="get">
                Logged in as ${request.user.username}.
                <input class="btn btn-info" type="submit" value="Sign out" />
              </form>
            %else:
              <form class="navbar-form" action="/login/github" method="post">
                <input class="btn btn-primary" type="submit" value="Sign in with Github" />
              </form>
            %endif
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="vspace"></div>

    <div class="container-fluid">
      ${self.body()}
    </div>
    <footer class="container-fluid">
    <p>Statatat is written by <a href="http://threebean.org">Ralph Bean</a>
      and is licened under the
      <a href="http://www.gnu.org/licenses/agpl-3.0.txt">AGPL</a>; the source
      code can be found
      <a href="http://github.com/ralphbean/statatat">on github.</a>
    </p>
    </footer>
  </body>
</html>
