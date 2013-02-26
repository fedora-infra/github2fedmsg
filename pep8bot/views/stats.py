from pyramid.view import view_config
import pep8bot.models as m
from sqlalchemy import or_


@view_config(route_name='stats', renderer='stats.mak')
def stats(request):
    """ Show the stats page """
    num_users = m.User.query.count()
    num_repos = m.Repo.query.count()
    num_enabled_repos = m.Repo.query.filter(or_(
        m.Repo.pep8_enabled==True,
        m.Repo.pylint_enabled==True,
        m.Repo.pyflakes_enabled==True,
        m.Repo.mccabe_enabled==True,
    )).count()

    # Show the top 'n' in various categories.
    n = 5

    latest_registered = m.User.query\
            .order_by(m.User.created_on.desc()).limit(n).all()

    all_users = m.User.query.all()
    by_total_enabled_repos = sorted(
        all_users,
        lambda x, y: cmp(x.total_enabled_repos, y.total_enabled_repos),
        reverse=True,
    )[:n]
    by_percent_enabled_repos = sorted(
        all_users,
        lambda x, y: cmp(x.percent_enabled_repos, y.percent_enabled_repos),
        reverse=True,
    )[:n]
    return locals()
