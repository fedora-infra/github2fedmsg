<%inherit file="master.mak"/>

<div class="content">
  <div class="row">
    <span class="span6 offset3">
      <h1>Stats</h1>
      <p>There are <strong>${num_users} registered users</strong> with <strong>${num_repos} total
          repositories.</strong></p>
      <p>Of those repositories, <strong>${num_enabled_repos} have the webhook
          enabled.</strong></p>
    </span>
  </div>

  <div class="row"><span class="span6 offset3">
      <h1>Latest 10 registered</h1>
      <table class="table table-condensed">
        <thead><tr>
            <th>#</th><th>User</th><th>Registered</th>
        </tr></thead>
        <tbody>
          % for i, user in enumerate(latest_registered):
            <tr>
              <td>${str(i+1)}</td>
              <td>
                <a href="/${user.username}">
                  <img src="${user.avatar}?s=20"/>
                  ${user.username}
                </a>
              </td>
              <td>${user.created_on_fmt}</td>
            </tr>
          % endfor
        </tbody>
      </table>
  </span></div>

  <div class="row"><span class="span6 offset3">
      <h1>Most repos enabled</h1>
      <table class="table table-condensed">
        <thead><tr>
            <th>#</th><th>User</th><th>Enabled Repos</th>
        </tr></thead>
        <tbody>
          % for i, user in enumerate(by_total_enabled_repos):
            <tr>
              <td>${str(i+1)}</td>
              <td>
                <a href="/${user.username}">
                  <img src="${user.avatar}?s=20"/>
                  ${user.username}
                </a>
              </td>
              <td>${user.total_enabled_repos}</td>
            </tr>
          % endfor
        </tbody>
      </table>
  </span></div>

  <div class="row"><span class="span6 offset3">
      <h1>Highest % repos enabled</h1>
      <table class="table table-condensed">
        <thead><tr>
            <th>#</th><th>User</th><th>Percent Enabled Repos</th>
        </tr></thead>
        <tbody>
          % for i, user in enumerate(by_percent_enabled_repos):
            <tr>
              <td>${str(i+1)}</td>
              <td>
                <a href="/${user.username}">
                  <img src="${user.avatar}?s=20"/>
                  ${user.username}
                </a>
              </td>
              <td>${user.percent_enabled_repos}%</td>
            </tr>
          % endfor
        </tbody>
      </table>
  </span></div>
</div>
