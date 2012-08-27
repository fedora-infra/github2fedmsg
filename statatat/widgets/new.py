import tw2.core as twc

class NewWidgetWidget(twc.Widget):
    template = "mako:statatat.widgets.templates.new"
    user = twc.Param("An instance of the User SQLAlchemy model.")
