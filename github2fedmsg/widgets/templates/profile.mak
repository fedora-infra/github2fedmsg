## -*- coding: utf-8 -*-
<div class="content">
  <div class="row">
    <span class="span10 offset1 profile-header">
      <div class="photo-64"><img src="${w.user.avatar}&s=64" /></div>
      <h1>
        ${w.user.username}
        <small>${w.user.full_name} ${len(w.user.all_repos)} repos</small>
      </h1>
    </span>


  </div>

% if w.show_buttons:
  <div class="row">
    <span class="offset6 span4">
    %if w.user.oauth_access_token:
    <form action="/forget_github_token" method="get">
      <input class="btn btn-primary" type="submit" value="Forget Github Auth" />
    </form>
    <form action="/api/${w.user.username}/sync" method="get">
      <input class="btn btn-warning" type="submit" value="Sync"/>
    </form>
    %else:
    <form action="/login/github">
      <input class="btn btn-info" type="submit" value="Link Github Auth"/>
    </form>
    %endif
    </span>
  </div>
% endif

  <div class="row">&nbsp;</div>

  <div class="row">
    <span class="span10 offset1">
      <table class="table table-condensed table-hover table-striped">
        <tr>
          <th>Name</th>
          <th>Description</th>
          <th>Language</th>
% if w.show_buttons:
          <th>Enabled?</th>
% endif
        </tr>
        % for repo in list(w.user.all_repos):
          <tr>
            <td>${repo.user.github_username}/${repo.name}</td>
            <td>${repo.description}</td>
            <td>${repo.language}</td>
% if w.show_buttons:
            <td>${w.make_button(repo) | n}</td>
% endif
          </tr>
        % endfor
      </table>
    </span>
  </div>
</div>
