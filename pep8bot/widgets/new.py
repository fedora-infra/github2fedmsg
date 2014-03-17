import tw2.core as twc
import tw2.bootstrap.forms as twb

#from pygithub3 import Github
#gh = Github()

class NoSpaces(twc.Validator):
    def validate(self, val):
        if ' ' or '\t' in val:
            raise twc.ValidationError("may not contain spaces")
        return val

class NewWidgetForm(twb.HorizontalForm):
    legend = twc.Param(default="")

    name = twb.TextField(validator=NoSpaces)

    # TODO -- uncomment this once we've got twb.SingleSelectField
    priority = twb.SingleSelectField(options=['', 'Normal', 'High'])
    space = twb.Spacer()
    description = twb.TextArea()
    buttons = [twb.SubmitButton, twb.ResetButton]


class NewWidgetWidget(twc.Widget):
    template = "mako:pep8bot.widgets.templates.new"
    user = twc.Param("An instance of the User SQLAlchemy model.")

    # These get filled in just before the widget is displayed.
    gh_user = twc.Variable()
    gh_repos = twc.Variable()

    child = NewWidgetForm(legend="New widget..")

    def prepare(self):
        """ Query github for some information before display """
        self.gh_user = gh.users.get(self.user.username)
        # Sort repos alphabetically by name
        self.gh_repos = sorted(
            gh.repos.list(self.user.username).all(),
            lambda x, y: cmp(x.name.lower(), y.name.lower()),
        )
