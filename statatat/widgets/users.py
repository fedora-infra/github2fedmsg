import tw2.core as twc

class UserProfile(twc.Widget):
    template = "mako:statatat.widgets.templates.profile"
    user = twc.Param("An instance of the User SQLAlchemy model.")
