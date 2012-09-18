<span class="profile-header">
<div class="photo-64"><img src="${w.gh_user.avatar_url}&s=64" /></div>
<h1>
  ${w.user.username}
  <small>${w.gh_user.name}, ${len(w.gh_repos)} repos</small>
</h1>
</span>

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
