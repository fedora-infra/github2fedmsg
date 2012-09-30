## -*- coding: utf-8 -*-
<div class="content">
  <div class="row">
    <span class="span10 offset1 profile-header">
      <div class="photo-64"><img src="${w.gh_user.avatar_url}&s=64" /></div>
      <h1>
        ${w.user.username}
        <small>${w.gh_user.name}, ${len(w.gh_repos)} repos</small>
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
        % for repo in w.gh_repos:
          <tr>
            <td>${repo.name}</td>
            <td>${repo.description}</td>
            <td>${repo.language}</td>
            <td>${w.make_button(repo.name)}</td>
          </tr>
        % endfor
      </table>
    </span>
  </div>
</div>
<div class="modal hide fade" id="widgets_modal" tabindex="-1" role="dialog" aria-labelledby="widgets_modal_label" aria-hidden="true">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="widgets_modal_label">Embeddable Widgets</h3>
  </div>
  <div class="modal-body">
    <p>Copy-and-paste any of the following into another webpage.</p>
    <p>Your commits <input value="${w.widget_link() | n}" /></p>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
  </div>
</div>
