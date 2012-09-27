<%inherit file="master.mak"/>

<div class="content">
  <div class="row">
    <span class="span6 offset3">
      <h1>Stats on <a href="http://statatat.threebean.org"
          class="brand">statatat</a></h1>
      <p>There are <strong>${num_users} registered users</strong> with <strong>${num_repos} total
          repositories.</strong></p>
      <p>Of those repositories, <strong>${num_enabled_repos} have the webhook
          enabled.</strong></p>
    </span>
  </div>
</div>
