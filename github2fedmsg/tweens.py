import tw2.core.core
import tw2.bootstrap.forms


def remove_bootstrap_factory(handler, registry):
    """ Remove tw2 bootstrap_css from tw2's middleware registry.

    In order to use this, you need to add the following to your
    myapp/__init__.py file:

        config.add_tween('myapp.tween.remove_bootstrap_factory')

    """

    def remove_bootstrap_tween(request):
        # Send the request on through to other tweens and to our app
        response = handler(request)

        # Before the response is modified by the tw2 middleware, let's remove
        # bootstrap_css from its registry.
        offending_links = [r.req().filename for r in [
            tw2.bootstrap.forms.bootstrap_css,
            tw2.bootstrap.forms.bootstrap_responsive_css,
        ]]
        local = tw2.core.core.request_local()
        local['resources'] = [
            r for r in local.get('resources', list())
            if r.filename not in offending_links
        ]

        return response

    return remove_bootstrap_tween
