<html>
  <head></head>
  <body>
    % if request.user:
      <span class="welcome">Welcome,
        <span class="username">${request.user.username}</span>
      </span>
      <span class="logout"><a href="/logout">Logout</a></span>
    % else:
      <form action="/login/github" method="post">
        <input type="submit" value="Login with Github" />
      </form>
      Hai there.
    % endif

    TODO - put stuff here about what this is, pictures of users using it and
    having fun.. etc.

    ${moksha_socket.display() | n}
  </body>
</html>
