## -*- coding: utf-8 -*-
<div class="content">
  <div class="row profile-header">
    <span class="col-md-1">
      <form method="POST" action="https://www.libravatar.org/openid/login/">
        <input type="hidden" name="openid_identifier" value="${w.user.openid_url}"/>
        <input type="image" class="img-circle centered"
               src="${w.user.avatar}&s=86" style="outline: none;"
               alt="${w.user.username}'s avatar"/>
      </form>
    </span>
    <span class="col-md-11">
      <h1>
        ${w.user.username}
        <small>${w.user.full_name}
        %if w.user.github_username:
          (${w.user.github_username} on github with ${len(w.user.all_repos)} repos)
        %else:
          (github account not linked)
        %endif
        </small>
      </h1>
    </span>
  </div>
  <div class="row profile-buttons">
    <span class="col-md-12">
      <a href="${w.request.route_url('logout')}" class="pull-right btn btn-default btn-sm">
        <span class="glyphicon glyphicon-log-out"></span>
        Sign out
      </a>
      % if w.show_buttons:
      %if w.user.oauth_access_token:
      <a href="${w.request.route_url('home')}api/${w.user.username}/sync" class="pull-right btn btn-default btn-sm">
        <span class="glyphicon glyphicon-refresh"></span>
        Refresh from Github
      </a>
      <a href="${w.request.route_url('forget_github_token')}" class="pull-right btn btn-default btn-sm">
        <span class="glyphicon glyphicon-floppy-remove"></span>
        Forget Github Authz
      </a>
      %else:
      <a href="${w.request.route_url('velruse.github-login')}" class="pull-right btn btn-default btn-sm">
        <span class="glyphicon glyphicon-transfer"></span>
        Link with Github
      </a>
      %endif
      % endif
    </span>
  </div>

  <div class="row">&nbsp;</div>

  <div class="row">
    <span class="col-md-10 col-md-offset-1">
      <table class="table table-condensed table-hover table-striped">
        <tr>
          <th>Name</th>
          <th>Description</th>
          <th>Language</th>
% if w.show_buttons and w.user.oauth_access_token:
          <th>Enabled?</th>
% endif
        </tr>
        % for repo in list(w.user.all_repos):
          <tr>
            <td>${repo.user.github_username}/${repo.name}</td>
            <td>${repo.description}</td>
            <td>${repo.language}</td>
% if w.show_buttons and w.user.oauth_access_token:
            <td>${w.make_button(repo) | n}</td>
% endif
          </tr>
        % endfor
      </table>
    </span>
  </div>
</div>
