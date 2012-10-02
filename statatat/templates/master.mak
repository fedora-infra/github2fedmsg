<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="stylesheet" type="text/css" href="/static/statatat.css" media="all"/>

    <script type="text/javascript">
      $.extend($.gritter.options, {
        position: 'bottom-left',
        fade_in_speed: 'medium',
        fade_out_speed: 500,
        time: 2500,
      });
    </script>
  </head>
  <body>
    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="brand" href="http://statatat.threebean.org">statatat</a>
          <ul class="nav pull-right">
            <li class="${['', 'active'][request.on_stats]}">
              <a href="/stats">Stats</a>
            </li>
            %if request.user:
              <li class="${['', 'active'][request.on_profile]}">
              <a href="/${request.user.username}">
                Profile
              </a>
              </li>
              <li class="">
                <a href="#widgets_modal" data-toggle="modal">Widgets</a>
              </li>
            %endif
            <li class="">
            %if request.user:
              <form class="navbar-form pull-right" action="/logout" method="get">
                <input class="btn btn-info" type="submit" value="Sign out" />
              </form>
            %else:
              <form class="navbar-form pull-right" action="/login/github" method="post">
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
    ${moksha_socket.display() |n }
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
