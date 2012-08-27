<html>
  <head></head>
  <body>
    <div class="header">
      <span class="logo">statat.at</span>
      %if request.user:
        Logged in as ${request.user.username}.
        <a href="/logout">[logout]</a>
      %else:
        <form action="/login/github" method="post">
          <input type="submit" value="Login with Github" />
        </form>
      %endif
    </div>

    ${self.body()}

    <div class="footer">
      Footer.
    </div>
  </body>
</html>
