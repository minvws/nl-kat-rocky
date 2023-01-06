from django.views.generic import TemplateView
from django.shortcuts import redirect


class LandingPageView(TemplateView):
    template_name = "landing_page.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("crisis_room")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = []

        return context
