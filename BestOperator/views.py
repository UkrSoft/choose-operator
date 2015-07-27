import datetime
from django.views.generic import TemplateView

class MainView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MainView, self).get_context_data(**kwargs)
        context['now'] = datetime.datetime.now()
        return context
