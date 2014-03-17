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
    <span class="span1 offset10">
      <button class="btn btn-warning" onclick="window.location = '/api/${w.user.username}/sync';">
        Sync..
      </button>
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
            <td>${repo.user.username}/${repo.name}</td>
            <td>${repo.description}</td>
            <td>${repo.language}</td>
% if w.show_buttons:
            <td>${w.make_button(repo.user.username, repo.name) | n}</td>
% endif
          </tr>
        % endfor
      </table>
    </span>
  </div>
</div>
