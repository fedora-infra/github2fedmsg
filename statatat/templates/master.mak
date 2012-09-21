<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="stylesheet" type="text/css" href="/static/statatat.css" media="all"/>
  </head>
  <body>
    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="brand" href="http://statatat.threebean.org">statatat</a>
          <ul class="nav pull-right">
            %if request.user:
              <li class="${['', 'active'][request.on_profile]}">
              <a href="/${request.user.username}">
                Profile
              </a>
              </li>
              <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                Widgets <b class="caret"></b>
              </a>
              <ul class="dropdown-menu" role="menu" aria-labelledby="dLabel">
                <li><a href="/${request.user.username}/new" tabindex="-1">
                  Create New...
                </a></li>
                % for conf in request.user.widget_configurations:
                  <li><a href="/${request.user.username}/%{conf.name}">
                    ${conf.name}
                  </a></li>
                % endfor
              </ul>
              </li>
            %endif
            <li class="">
            %if request.user:
              <form class="navbar-form pull-right" action="/logout" method="get">
                <input class="btn btn-info" type="submit" value="Sign out" />
              </form>
            %else:
              <form class="navbar-form pull-right" action="/login/github" method="post">
                <input class="btn btn-inverse" type="submit" value="Sign in with Github" />
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
