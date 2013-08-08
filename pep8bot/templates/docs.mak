<%inherit file="master.mak"/>

<div class="content">
  <div class="row">
    <span class="span6 offset3">
      <h1>"Docs"</h1>
      <p>
      <a href="http://pep8.me">pep8bot</a> works by installing
      webhooks in your github repositories.  Whenever someone pushes commits
      and issues a pull request on one of yours, <a
      href="http://pep8.me">pep8bot</a> will be notified of the
      event, will pull that code down, and then run a series of
      checks.  The results are posted by using github's "Status
      API", much like the popular Travis-CI.
      </p>
      <p>
      If you want to enable or disable certain pep8 checks, you can
      add a <code>[pep8]</code> section to a
      <code>setup.cfg</code> and <a href="http://pep8.me">pep8bot</a> will
      obey those exceptions.  </p>
      <p>For instance, if you setup your <code>setup.cfg</code> to look like
      this, <a href="http://pep8.me">pep8bot</a> will ignore error number
      126</p>
    <pre>
    [pep8]
    ignore=E126
    </pre>
    </span>
  </div>
</div>
