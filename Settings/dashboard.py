from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
from core.dashboard_modules import Nombre_budgetenreg




class CustomIndexDashboard(Dashboard):
    columns = 1
    def init_with_context(self, context):
        self.available_children=[Nombre_budgetenreg,modules.LinkList]


        self.children=[
            Nombre_budgetenreg(_('Nombre Total de budgets enregistés')),

        ]

        self.children.append(modules.AppList(
            _('Modules'),
            exclude=('auth.*',),
            column=2,
            order=0
        ))
        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('auth.*',),
            column=2,
            order=0
        ))