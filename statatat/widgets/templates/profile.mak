<div class="photo-64"><img src="${w.gh_user.avatar_url}" /></div>
<span class="main name">
  ${w.user.username}
  (${w.gh_user.name}))
  ${len(w.gh_repos)} repos
</span>

<table class="table table-condensed table-hover table-striped">
  <tr>
    <th>Name</th>
    <th>Description</th>
    <th>Language</th>
    <th>Enable</th>
  </tr>
  % for repo in w.gh_repos:
    <tr>
      <td>${repo.name}</td>
      <td>${repo.description}</td>
      <td>${repo.language}</td>
      <td>button goes here</td>
    </tr>
  % endfor
</table>
