<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="stylesheet" type="text/css" href="/static/pep8bot.css" media="all"/>
    <script type="text/javascript">
      $.extend($.gritter.options, {
        position: 'bottom-left',
        fade_in_speed: 'medium',
        fade_out_speed: 500,
        time: 2500,
      });
    </script>
    <script type="text/javascript">
      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', 'UA-1943020-6']);
      _gaq.push(['_trackPageview']);
      (function() {
        var ga = document.createElement('script');
        ga.type = 'text/javascript';
        ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(ga, s);
      })();
    </script>
  </head>
  <body>
    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="brand" href="http://pep8.me">pep8.me</a>
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

    %if request.user:
    <div class="modal hide fade" id="widgets_modal" tabindex="-1" role="dialog" aria-labelledby="widgets_modal_label" aria-hidden="true">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
        <h3 id="widgets_modal_label">Embeddable Widgets</h3>
      </div>
      <div class="modal-body">
        <p>Copy-and-paste the following into another webpage.</p>
        <p>Your commits <input value="${request.user.widget_link() | n}" /></p>
      </div>
      <div class="modal-footer">
        <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
      </div>
    </div>
    %endif

    ${moksha_socket.display() |n }

    <footer class="container-fluid">
    <p>Pep8Bot is written by <a href="http://threebean.org">Ralph Bean</a>
      and is licened under the
      <a href="http://www.gnu.org/licenses/agpl-3.0.txt">AGPL</a>; the source
      code can be found
      <a href="http://github.com/ralphbean/pep8bot">on github.</a>
    </p>
    </footer>

  </body>
</html>
