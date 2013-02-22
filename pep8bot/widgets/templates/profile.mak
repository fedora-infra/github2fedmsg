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

  <div class="row">
    <span class="span10 offset1">
      <table class="table table-condensed table-hover table-striped">
        <tr>
          <th>Name</th>
          <th>Description</th>
          <th>Language</th>
          <th>Hook?</th>
        </tr>
        % for repo in list(w.user.all_repos):
          <tr>
            <td>${repo.user.username}/${repo.name}</td>
            <td>${repo.description}</td>
            <td>${repo.language}</td>
            <td>${w.make_button(repo.user.username, repo.name) | n}</td>
          </tr>
        % endfor
      </table>
    </span>
  </div>
</div>
