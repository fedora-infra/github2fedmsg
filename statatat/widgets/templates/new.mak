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
      ${w.child.display()}
    </span>
  </div>
</div>
