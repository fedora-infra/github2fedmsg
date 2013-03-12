<%inherit file="master.mak"/>

<div class="content">
  <div class="row">
    <span class="span6 offset3">
      <h1>${commit.repo.user.username}/${commit.repo.name}
	  <small>${commit.sha} <a href="${commit.url}">(View on GitHub)</a>
	  </small></h3>
    </span>
  </div>

%for kind in ['pep8', 'pylint', 'pyflakes']:
  <div class="row">
    <span class="span6 offset4">
	% if getattr(commit.repo, kind + "_enabled"):
		<h2>${kind} -- ${str(getattr(commit, kind + "_error_count"))} errors</h2>
<pre>${str(getattr(commit, kind + "_errors"))}</pre>
	% else:
		<h2>${kind} <code>disabled</code></h2>
	% endif
    </span>
  </div>
%endfor

</div>
