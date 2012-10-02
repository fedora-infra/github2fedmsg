from pyramid.view import view_config
import statatat.models as m


@view_config(route_name='stats', renderer='stats.mak')
def stats(request):
    """ Show the stats page """
    num_users = m.User.query.count()
    num_repos = m.Repo.query.count()
    num_enabled_repos = m.Repo.query.filter_by(enabled=True).count()

    # Show the top 'n' in various categories.
    n = 5

    latest_registered = m.User.query\
            .order_by(m.User.created_on.desc()).limit(n).all()

    all_users = m.User.query.all()
    by_total_enabled_repos = sorted(
        all_users,
        lambda x, y: cmp(x.total_enabled_repos, y.total_enabled_repos)
    )[:n]
    by_percent_enabled_repos = sorted(
        all_users,
        lambda x, y: cmp(x.percent_enabled_repos, y.percent_enabled_repos)
    )[:n]
    return locals()
