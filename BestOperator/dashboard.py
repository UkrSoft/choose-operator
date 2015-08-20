"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'choose_operator.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'choose_operator.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for choose_operator.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=True,
            deletable=True,
            collapsible=True,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        self.children.append(
            modules.ModelList(
                title = _('Operators/Packages'),
                models = (
                    'BestOperator.models.Operator',
                    'BestOperator.models.Code',
                    'BestOperator.models.Package',
                ),
            )
        )
        self.children.append(
            modules.ModelList(
                title = _('Offers/Features'),
                models = (
                    'BestOperator.models.Offer',
                    'BestOperator.models.Feature',
                    'BestOperator.models.Param',
                    'BestOperator.models.Attribute',
                ),
            )
        )
        self.children.append(
            modules.ModelList(
                title = _('Services'),
                models = (
                    'BestOperator.models.Service',
                    'BestOperator.models.Direction',
                    'BestOperator.models.Location',
                ),
            )
        )
        self.children.append(
            modules.ModelList(
                title = _('Terms / Payments'),
                models = (
                    'BestOperator.models.POTerm',
                    'BestOperator.models.Payment',
                    'BestOperator.models.Period',
                    'BestOperator.models.TermOfUsage',
                ),
            )
        )
        self.children.append(
            modules.ModelList(
                title = _('Supplementary'),
                models = (
                    'BestOperator.models.Directory',
                    'BestOperator.models.ServiceType',
                    'BestOperator.models.LocationType',
                    'BestOperator.models.PackageType',
                    'BestOperator.models.Criterion',
                ),
            )
        )
        # append an app list module for "Administration"
        # self.children.append(modules.AppList(
        #     _('Site Administration'),
        #     models=('django.contrib.*',),
        # ))

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for choose_operator.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)
        self.children = CustomIndexDashboard().children
        # append a model list module and a recent actions module
        self.children += [
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=10
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
