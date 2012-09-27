from pyramid.view import view_config
import statatat.models as m


@view_config(route_name='stats', renderer='stats.mak')
def stats(request):
    """ Show the stats page """
    num_users = m.User.query.count()
    num_repos = m.Repo.query.count()
    num_enabled_repos = m.Repo.query.filter_by(enabled=True).count()
    return locals()
